
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

	@staticmethod
	def ffb_packet_to_dict(data,reptype : int):
		"""Helper function to convert FFB packets into named python dicts. 
		Returns dict with single named entry and effect block index if applicable. 
		Otherwise ebi is 0 for control reports"""

		packetnames = [None,"effect","envelope","cond","period","const","ramp","custom","sample",None,"effop","blkfree","ctrl","gain","setcustom",None,"neweff","blkload","pool"]
		if reptype >= len(packetnames):
			return None,0
		
		typename = packetnames[reptype]
		if reptype == _sdk.PT_CONDREP:
			typename += "Y" if data["isY"] else "X"
		ebi = 0
		if isinstance(data,_sdk.PacketStruct):
			data = data.to_dict()
			if "EffectBlockIndex" in data:
				ebi = data["EffectBlockIndex"]
		ret = {typename:data}
		
		return ret,ebi