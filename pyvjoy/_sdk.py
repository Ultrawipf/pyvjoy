import os
import sys
from ctypes import *


from pyvjoy.constants import *
from pyvjoy.exceptions import *

from ctypes import wintypes	# Makes this lib work in Python36

# Check if 32bit or 64
if sys.maxsize > 2**32:
    arch_folder = 'lib' + os.sep + 'x64'
else:
    arch_folder = 'lib' + os.sep + 'x86'

dll_path = os.path.dirname(__file__) + os.sep + arch_folder + os.sep + DLL_FILENAME

try:
	_vj = cdll.LoadLibrary(dll_path)
except OSError:
	sys.exit("Unable to load vJoy SDK DLL.  Ensure that %s is present" % DLL_FILENAME)


def vJoyEnabled():
	"""Returns True if vJoy is installed and enabled"""

	result = _vj.vJoyEnabled()

	if result == 0:
		raise vJoyNotEnabledException()
	else:
		return True


def DriverMatch():
	"""Check if the version of vJoyInterface.dll and the vJoy Driver match"""
	result = _vj.DriverMatch()
	if result == 0:
		raise vJoyDriverMismatch()
	else:
		return True


def GetVJDStatus(rID):
	"""Get the status of a given vJoy Device"""

	return _vj.GetVJDStatus(rID)


def AcquireVJD(rID):
	"""Attempt to acquire a vJoy Device"""

	result = _vj.AcquireVJD(rID)
	if result == 0:
		#Check status
		status = GetVJDStatus(rID)
		if status != VJD_STAT_FREE:
			raise vJoyFailedToAcquireException("Cannot acquire vJoy Device because it is not in VJD_STAT_FREE")

		else:
			raise vJoyFailedToAcquireException()

	else:
		return True


def RelinquishVJD(rID):
	"""Relinquish control of a vJoy Device"""

	result = _vj.RelinquishVJD(rID)
	if result == 0:
		raise vJoyFailedToRelinquishException()
	else:
		FfbRemoveCB(rID) # Also delete FFB callback if present
		return True


def SetBtn(state,rID,buttonID):
	"""Sets the state of a vJoy Button to on or off.  SetBtn(state,rID,buttonID)"""
	result = _vj.SetBtn(state,rID,buttonID)
	if result == 0:
		raise vJoyButtonException()
	else:
		return True

def SetAxis(AxisValue,rID,AxisID):
	"""Sets the value of a vJoy Axis  SetAxis(value,rID,AxisID)"""

	#TODO validate AxisID
	#TODO validate AxisValue

	result = _vj.SetAxis(AxisValue,rID,AxisID)
	if result == 0:
		#TODO raise specific exception
		raise vJoyException()
	else:
		return True




def SetDiscPov(PovValue, rID, PovID):
	"""Write Value to a given discrete POV defined in the specified VDJ"""
	if PovValue < -1 or PovValue > 3:
		raise vJoyInvalidPovValueException()

	if PovID < 1 or PovID > 4:
		raise vJoyInvalidPovIDException

	return _vj.SetDiscPov(PovValue,rID,PovID)


def SetContPov(PovValue, rID, PovID):
	"""Write Value to a given continuous POV defined in the specified VDJ"""
	if PovValue < -1 or PovValue > 35999:
		raise vJoyInvalidPovValueException()

	if PovID < 1 or PovID > 4:
		raise vJoyInvalidPovIDException

	return _vj.SetContPov(PovValue,rID,PovID)



def ResetVJD(rID):
	"""Reset all axes and buttons to default for specified vJoy Device"""
	return _vj.ResetVJD(rID)


def ResetButtons(rID):
	"""Reset all buttons to default for specified vJoy Device"""
	return _vj.ResetButtons(rID)


def ResetPovs(rID):
	"""Reset all POV hats to default for specified vJoy Device"""
	return _vj.ResetPovs(rID)

	
def UpdateVJD(rID, data):
	"""Pass data for all buttons and axes to vJoy Device efficiently"""
	return _vj.UpdateVJD(rID, pointer(data))

	
def CreateDataStructure(rID):
	data = _JOYSTICK_POSITION_V2()
	data.set_defaults(rID)
	return data
	
	
class _JOYSTICK_POSITION_V2(Structure):
	_fields_ = [
	('bDevice', c_byte),
	('wThrottle', c_long),
	('wRudder', c_long),
	('wAileron', c_long),
	('wAxisX', c_long),
	('wAxisY', c_long),
	('wAxisZ', c_long),
	('wAxisXRot', c_long),
	('wAxisYRot', c_long),
	('wAxisZRot', c_long),
	('wSlider', c_long),
	('wDial', c_long),
	('wWheel', c_long),
	('wAxisVX', c_long),
	('wAxisVY', c_long),
	('wAxisVZ', c_long),
	('wAxisVBRX', c_long),
	('wAxisVRBY', c_long),
	('wAxisVRBZ', c_long),
	('lButtons', c_long), # 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
	
	('bHats', wintypes.DWORD ),		# Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
	('bHatsEx1', wintypes.DWORD ),		# Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
	('bHatsEx2', wintypes.DWORD ),		# Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
	('bHatsEx3', wintypes.DWORD ),		# Lower 4 bits: HAT switch or 16-bit of continuous HAT switch LONG lButtonsEx1
	
	# JOYSTICK_POSITION_V2 Extension
	
	('lButtonsEx1', c_long),	# Buttons 33-64	
	('lButtonsEx2', c_long), # Buttons 65-96
	('lButtonsEx3', c_long), # Buttons 97-128
	]
	
	def set_defaults(self, rID):
		
		self.bDevice=c_byte(rID)
		self.bHats=-1
		
 

# FFB:
class PacketStruct(Structure):
	def to_dict(self):
		return dict((field, getattr(self, field)) for field, _ in self._fields_ if field)
	def keys(self):
		return [field for field, _ in self._fields_ if field]
	def __getitem__(self,key):
		return getattr(self, key)
	def values(self):
		return [getattr(self, field) for field, _ in self._fields_ if field]
	def __str__(self):
		return str(self.to_dict())

class _FFB_DATA(Structure):
	_fields_ = [
	('size', c_ulong),
	('cmd', c_ulong),
	('data', c_void_p),
	]

class _FFB_EFFECT(PacketStruct):
	_pack_ = 1
	_fields_ = [
		('EffectBlockIndex',c_uint32),
		('EffectType',c_uint32),
		('Duration',c_uint16),
		('TriggerRpt',c_uint16),
		('SamplePrd',c_uint16),
		('Gain',c_ubyte),
		('TriggerBtn',c_ubyte),
		('Polar',c_uint32), # Bool but 4 bytes padded
		('DirX',c_byte), # Polar direction or dirX depending on Polar bool
		('DirY',c_byte),
	]


class _FFB_EFF_RAMP(PacketStruct):
	_pack_ = 1
	_fields_ = [
		('EffectBlockIndex',c_uint32),
		('Start',c_int16),
		('',c_int16), # Reserved padding
		('End',c_int16),
	]


class _FFB_EFF_OP(PacketStruct):
	_pack_ = 1
	_fields_ = [
		('EffectBlockIndex',c_uint32),
		('EffectOp',c_uint32),
		('LoopCount',c_uint32),
	]


class _FFB_EFF_PERIOD(PacketStruct):
	_pack_ = 1
	_fields_ = [
		('EffectBlockIndex',c_uint32),
		('Magnitude',c_uint32),
		('Offset',c_int16),
		('',c_int16), # Padding
		('Phase',c_uint32),
		('Period',c_uint32),
	]


class _FFB_EFF_COND(PacketStruct):
	_pack_ = 1
	_fields_ = [
		('EffectBlockIndex',c_uint32),
		('isY',c_uint32),
		('CenterPointOffset',c_int16),
		('',c_int16), # Padding
		('PosCoeff',c_int16),
		('',c_int16), # Padding
		('NegCoeff',c_int16),
		('',c_int16), # Padding
		('PosSatur',c_uint32),
		('NegSatur',c_uint32),
		('DeadBand',c_int32),
	]


class _FFB_EFF_ENVLP(PacketStruct):
	_pack_ = 1
	_fields_ = [
		('EffectBlockIndex',c_uint32),
		('AttackLevel',c_uint32),
		('FadeLevel',c_uint32),
		('AttackTime',c_uint32),
		('FadeTime',c_uint32),
	]


class _FFB_EFF_CONST(PacketStruct):
	_pack_ = 1
	_fields_ = [
		('EffectBlockIndex',c_uint32),
		('Magnitude',c_int16),
	]


class FFBCallback():
	"""Helper class for FFB callbacks between python and vjoy"""
	vJoy_ffb_callback = None # Workaround to store callback functions
	
	def __init__(self):
		self.callbacks = {}
		self.internalcbtype = CFUNCTYPE(None,_FFB_DATA, c_void_p)

		# Callback can not be a member function
		def ffbCallback(ffbpacket,userdata):
			"""Helper callback passed to vjoy. Will call previously registered python function with parsed FFB data"""
			parsedData,reptype,devid = FFBCallback._parse_ffb_packet(ffbpacket)
			if parsedData and (devid in self.callbacks):
				# packet,typename = self.packet_to_dict(reptype,parsedData)
				self.callbacks[devid](parsedData,reptype)
			
		self._internalcb = self.internalcbtype(ffbCallback)

	def addCallback(self,callback,rID):
		"""Add callback to rID device. Gets called when FFB data for rID is received"""
		self.callbacks[rID] = callback

	def removeCallback(self,rID):
		"""Remove rID from internal callback dict"""
		if rID in self.callbacks:
			del self.callbacks[rID]

	@staticmethod
	def _parse_ffb_packet(ffbpacket : _FFB_DATA):
		"""Helper function parse ffb data using vjoy functions"""
		t = c_int(0)
		res = _vj.Ffb_h_Type(ffbpacket, pointer(t))
		reptype = t.value
		if res != 0: # Invalid packet
			return None,0,0
		
		devid = c_int(0)
		_vj.Ffb_h_DeviceID(ffbpacket,pointer(devid)) # ID of vjoy device

		parsedPacket = None

		# Parse report type
		if reptype == PT_CTRLREP: # Control rep
			ctrl = c_int(0)
			if _vj.Ffb_h_DevCtrl(ffbpacket,pointer(ctrl)) == 0:
				parsedPacket = ctrl.value

		elif reptype == PT_EFFREP: # Set effect rep
			tstruct = _FFB_EFFECT()
			if _vj.Ffb_h_Eff_Report(ffbpacket,pointer(tstruct)) == 0:
				parsedPacket = tstruct

		elif reptype == PT_RAMPREP: # Ramp rep
			tstruct = _FFB_EFF_RAMP()
			if _vj.Ffb_h_Eff_Ramp(ffbpacket,pointer(tstruct)) == 0:
				parsedPacket = tstruct

		elif reptype == PT_EFOPREP: # EffOp rep
			tstruct = _FFB_EFF_OP()
			if _vj.Ffb_h_EffOp(ffbpacket,pointer(tstruct)) == 0:
				parsedPacket = tstruct

		elif reptype == PT_PRIDREP: # EffPeriod rep
			tstruct = _FFB_EFF_PERIOD()
			if _vj.Ffb_h_Eff_Period(ffbpacket,pointer(tstruct)) == 0:
				parsedPacket = tstruct

		elif reptype == PT_CONDREP: # Conditional rep
			tstruct = _FFB_EFF_COND()
			if _vj.Ffb_h_Eff_Cond(ffbpacket,pointer(tstruct)) == 0:
				parsedPacket = tstruct

		elif reptype == PT_ENVREP: # Envelope rep
			tstruct = _FFB_EFF_ENVLP()
			if _vj.Ffb_h_Eff_Envlp(ffbpacket,pointer(tstruct)) == 0:
				parsedPacket = tstruct

		elif reptype == PT_NEWEFREP: # NewEff rep
			neweff = c_int(0)
			if _vj.Ffb_h_EffNew(ffbpacket,pointer(neweff)) == 0:
				parsedPacket = neweff.value

		elif reptype == PT_CONSTREP: # Constant force rep
			tstruct = _FFB_EFF_CONST()
			if _vj.Ffb_h_Eff_Constant(ffbpacket,pointer(tstruct)) == 0:
				parsedPacket = tstruct

		elif reptype == PT_GAINREP: # Gain rep
			gainrep = c_int(0)
			if _vj.Ffb_h_DevGain(ffbpacket,pointer(gainrep)) == 0:
				parsedPacket = gainrep.value

		elif reptype == PT_BLKFRREP: # Block free rep
			blk = c_int(0)
			if _vj.Ffb_h_EBI(ffbpacket,pointer(blk)) == 0:
				parsedPacket = blk.value

		return parsedPacket,reptype,devid.value
	
	def getCcallback(self):
		"""Helper function returning the external C-type callback"""
		return self._internalcb

def FfbRegisterGenCB(func,rID):
	"""Registers a python FFB callback and translates packets"""
	if not FFBCallback.vJoy_ffb_callback:
		FFBCallback.vJoy_ffb_callback = FFBCallback()

	FFBCallback.vJoy_ffb_callback.addCallback(func,rID)
	devid = c_int(rID)
	_vj.FfbRegisterGenCB(FFBCallback.vJoy_ffb_callback.getCcallback(),pointer(devid))

def FfbRemoveCB(rID):
	"""Removes a callback from the helper class"""
	if FFBCallback.vJoy_ffb_callback:
		FFBCallback.vJoy_ffb_callback.removeCallback(rID)

def vJoyFfbCap():
	"""Returns True if vjoy is FFB capable"""
	ret = c_bool(False)
	_vj.vJoyFfbCap(pointer(ret))
	return ret.value

def IsDeviceFfb(rID):
	"""Returns True if device is FFB capable"""
	return _vj.IsDeviceFfb(rID) != 0

def IsDeviceFfbEffect(rID, effect):
	"""Returns True if device supports effect usage type"""
	return _vj.IsDeviceFfbEffect(rID,effect) != 0
