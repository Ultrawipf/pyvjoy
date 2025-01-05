
from pyvjoy.constants import *
from pyvjoy.exceptions import *

import pyvjoy._sdk as _sdk

class VJoyDevice(object):
	"""Object-oriented API for a vJoy Device"""

	def __init__(self,rID=None, data=None):
		"""Constructor"""

		self.rID=rID
		self._sdk=_sdk
		self._vj=self._sdk._vj

		if data:
			self.data = data
		else:
			#TODO maybe - have self.data as a wrapper object containing the Struct
			self.data = self._sdk.CreateDataStructure(self.rID)

		try:
			_sdk.vJoyEnabled()
			_sdk.AcquireVJD(rID)

		#TODO FIXME
		except vJoyException:
			raise

			
	def set_button(self,buttonID,state):
		"""Set a given button (numbered from 1) to On (1 or True) or Off (0 or False)"""
		return self._sdk.SetBtn(state,self.rID,buttonID)

		
	def set_axis(self,AxisID, AxisValue):
		"""Set a given Axis (one of pyvjoy.HID_USAGE_X etc) to a value (0x0000 - 0x8000)"""
		return self._sdk.SetAxis(AxisValue,self.rID,AxisID)
		
	def set_disc_pov(self, PovID, PovValue):
		return self._sdk.SetDiscPov(PovValue, self.rID, PovID)

	def set_cont_pov(self, PovID, PovValue):
		return self._sdk.SetContPov(PovValue, self.rID, PovID)

	def reset(self):
		"""Reset all axes and buttons to default values"""
			
		return self._sdk.ResetVJD(self.rID)

		
	def reset_data(self):
		"""Reset the data Struct to default (does not change vJoy device at all directly)"""
		self.data=self._sdk.CreateDataStructure(self.rID)
			
		
	def reset_buttons(self):
		"""Reset all buttons on the vJoy Device to default"""
		return self._sdk.ResetButtons(self.rID)

		
	def reset_povs(self):
		"""Reset all Povs on the vJoy Device to default"""
		return self._sdk.ResetPovs(self.rID)

		
	def update(self):
		"""Send the stored Joystick data to the device in one go (the 'efficient' method)"""
		return self._sdk.UpdateVJD(self.rID, self.data)

		
	def __del__(self):
		# free up the controller before losing access
		self._sdk.RelinquishVJD(self.rID)
		
		
	def ffb_supported(self):
		"""Returns True if device is FFB capable"""
		return self._sdk.vJoyFfbCap() and self._sdk.IsDeviceFfb(self.rID)
	
	def ffb_effect_supported(self,effect):
		"""Returns True if device supports effect usage type"""
		return self._sdk.IsDeviceFfbEffect(self.rID,effect)
	
	def ffb_register_callback(self,callback):
		"""Registers a callback for FFB data for this device"""
		self._sdk.FfbRegisterGenCB(callback,self.rID)



class FFB_Effect_Manager():
	"""Helper class that stores the current state of all effects and handles callbacks"""
	PACKET_TO_NAME = [None,"effect","envelope","cond","period","const","ramp","custom",
					  "sample",None,"effop","blkfree","ctrl","gain","setcustom",None,
					  "neweff","blkload","pool"]
	EFFECTTYPE_TO_NAME = ["None","Const","Ramp","Square","Sine","Triangle","SawtoothUp",
					  "SawtoothDown","Spring","Damper","Inertia","Friction","Custom"]

	def __init__(self):
		self.effects = []  # Effect storage. vjoy 2.2.x now supports multiple effect blocks

	def update_packet_cb(self,data,reptype,idx):
		"""Called after every ffb update to update internal dict. 
		Override to modify if internal state updating is not required"""
		packetdict,ebi = FFB_Effect_Manager.ffb_packet_to_dict(data,reptype)
		if len(self.effects) <= idx: # Extend effect storage
			self.effects.extend([{} for _ in range(1+idx-len(self.effects) ) ] )

		self.effects[idx].update(packetdict)
		self.update_effect_dict_cb(packetdict,idx)
		return
	
	def update_effect_dict_cb(self,packetdict,idx):
		"""Called after every ffb update with parsed dict by update_packet_cb"""
		return
	
	def update_ctrl_cb(self,ctrl):
		"""Control packet callback. Value can be any CTRL_ constant"""
		return
	
	def update_gain_cb(self,gain):
		"""Gain packet callback. Device gain 0-255"""
		return
	
	def update_effect_op_cb(self,enabled,idx):
		"""Change effect state callback"""
		return
	
	def update_effect_cb(self,data,idx):
		"""Set effect (effect) callback"""
		return
	
	def update_envelope_cb(self,data,idx):
		"""Set envelope callback"""
		return
	
	def update_condition_cb(self,data,idx):
		"""Set condition (condX or condY) callback"""
		return
	
	def update_periodic_cb(self,data,idx):
		"""Set periodic callback"""
		return
	
	def update_constant_cb(self,data,idx):
		"""Set constant force callback"""
		return
	
	def update_ramp_cb(self,data,idx):
		"""Set ramp callback"""
		return


	def __ffb_cb(self,data,reptype):
		"""Callback handling raw sdk data"""
		if reptype == PT_BLKFRREP: # Delete block
			self.effects[data-1].clear()

		if reptype == PT_CTRLREP:
			if(data == CTRL_DEVRST):
				self.effects.clear() # Reset clears all effects
			elif(data == CTRL_STOPALL):
				for e in self.effects:
					if "effop" in e:
						e["effop"]["EffectOp"] = EFF_STOP
						self.update_effect_op_cb(False,e["effop"]["EffectBlockIndex"])

			self.update_ctrl_cb(data)

		ebi = getattr(data,"EffectBlockIndex",0)
		if ebi: # Packet specifies effect block index
			self.update_packet_cb(data,reptype,ebi-1)

			if reptype == PT_EFOPREP:
				self.update_effect_op_cb((data.EffectOp != EFF_STOP),ebi-1)
			elif reptype == PT_EFFREP:
				self.update_effect_cb(data,ebi-1)
			elif reptype == PT_ENVREP:
				self.update_envelope_cb(data,ebi-1)
			elif reptype == PT_CONDREP:
				self.update_condition_cb(data,ebi-1)
			elif reptype == PT_PRIDREP:
				self.update_periodic_cb(data,ebi-1)
			elif reptype == PT_CONSTREP:
				self.update_constant_cb(data,ebi-1)
			elif reptype == PT_RAMPREP:
				self.update_ramp_cb(data,ebi-1)

		elif reptype == PT_GAINREP:
			self.update_gain_cb(data)

	def ffb_register_callback(self,j : VJoyDevice):
		"""Registers this class as the ffb callback for vjoy device j"""
		j.ffb_register_callback(self.__ffb_cb)

	@staticmethod
	def ffb_packet_to_dict(data,reptype : int):
		"""Helper function to convert FFB packets into named python dicts. 
		Returns dict with single named entry and effect block index if applicable. 
		Otherwise ebi is 0 for control reports"""

		if reptype >= len(FFB_Effect_Manager.PACKET_TO_NAME):
			return None,0
		
		typename = FFB_Effect_Manager.PACKET_TO_NAME[reptype]
		if reptype == _sdk.PT_CONDREP:
			typename += "Y" if data["isY"] else "X"
		ebi = 0
		if isinstance(data,_sdk.PacketStruct):
			data = data.to_dict()
			if "EffectBlockIndex" in data:
				ebi = data["EffectBlockIndex"]
		ret = {typename:data}
		return ret,ebi

	@staticmethod
	def effect_get_state(effect : dict):
		"""Gets the current state of an effect dict. False if stopped, True otherwise"""
		return effect.get("effop",{}).get("EffectOp",EFF_STOP) != EFF_STOP
	
	@staticmethod
	def get_effect_name(effect : dict):
		"""Extracts effect name from effect dict"""
		return FFB_Effect_Manager.EFFECTTYPE_TO_NAME[effect['effect'].get('EffectType',0)]

	@staticmethod
	def print_effect(effect):
		"""Helper function to print a single effect dict"""
		if effect and "effect" in effect:
			effectname = FFB_Effect_Manager.get_effect_name(effect)
			state = FFB_Effect_Manager.effect_get_state(effect)
			print(f"Type: {effectname}, State: {state}, Data: {effect}")

	@staticmethod
	def print_effects(effects):
		"""Helper function to print all current effect data"""
		for effect in effects:
			FFB_Effect_Manager.print_effect(effect)