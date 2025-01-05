DLL_FILENAME = "vJoyInterface.dll"

HID_USAGE_X = 0x30
HID_USAGE_Y	= 0x31
HID_USAGE_Z	= 0x32
HID_USAGE_RX = 0x33
HID_USAGE_RY = 0x34
HID_USAGE_RZ = 0x35
HID_USAGE_SL0 = 0x36
HID_USAGE_SL1 = 0x37
HID_USAGE_WHL = 0x38
HID_USAGE_POV = 0x39

#for validity checking
HID_USAGE_LOW = HID_USAGE_X
HID_USAGE_HIGH = HID_USAGE_POV


VJD_STAT_OWN = 0	# The  vJoy Device is owned by this application.
VJD_STAT_FREE = 1 	# The  vJoy Device is NOT owned by any application (including this one).
VJD_STAT_BUSY = 2   # The  vJoy Device is owned by another application. It cannot be acquired by this application.
VJD_STAT_MISS = 3 	# The  vJoy Device is missing. It either does not exist or the driver is down.
VJD_STAT_UNKN = 4 	# Unknown

# FFB rep
PT_EFFREP	=  0x01       # Usage Set Effect Report
PT_ENVREP	=  0x02       # Usage Set Envelope Report
PT_CONDREP	=  0x03       # Usage Set Condition Report
PT_PRIDREP	=  0x04       # Usage Set Periodic Report
PT_CONSTREP	=  0x05       # Usage Set Constant Force Report
PT_RAMPREP	=  0x06       # Usage Set Ramp Force Report
PT_CSTMREP	=  0x07       # Usage Custom Force Data Report
PT_SMPLREP	=  0x08       # Usage Download Force Sample
PT_EFOPREP	=  0x0A       # Usage Effect Operation Report
PT_BLKFRREP	=  0x0B       # Usage PID Block Free Report
PT_CTRLREP	=  0x0C       # Usage PID Device Control
PT_GAINREP	=  0x0D       # Usage Device Gain Report
PT_SETCREP	=  0x0E       # Usage Set Custom Force Report

# FFB feature rep
PT_NEWEFREP	=  0x01+0x10  # Usage Create New Effect Report
PT_BLKLDREP	=  0x02+0x10  # Usage Block Load Report
PT_POOLREP	=  0x03+0x10  # Usage PID Pool Report


# Effect Type
ET_NONE		=	0   #   No Force
ET_CONST	=	1   #   Constant Force
ET_RAMP		=	2   #   Ramp
ET_SQR		=	3   #   Square
ET_SINE		=	4   #   Sine
ET_TRNGL	=	5   #   Triangle
ET_STUP		=	6   #   Sawtooth Up
ET_STDN		=	7   #   Sawtooth Down
ET_SPRNG	=	8   #   Spring
ET_DMPR		=	9   #   Damper
ET_INRT		=	10  #   Inertia
ET_FRCTN	=	11  #   Friction
ET_CSTM 	=	12  #   Custom Force Data


# Effect operation
EFF_START	= 1 # EFFECT START
EFF_SOLO	= 2 # EFFECT SOLO START
EFF_STOP	= 3 # EFFECT STOP


# FFB ctrl
CTRL_ENACT      = 1 #  Enable all device actuators.
CTRL_DISACT     = 2 #  Disable all the device actuators.
CTRL_STOPALL    = 3 #  Stop All Effects:­ Issues a stop on every running effect.
CTRL_DEVRST     = 4 #  Device Reset: Clears any device paused condition, enables all actuators and clears all effects from memory.
CTRL_DEVPAUSE   = 5 #  Pause: All effects on the device are paused at the current time step.
CTRL_DEVCONT    = 6 #  Device Continue: The all effects that running when the device was paused are restarted from their last time step.

# HID effect usage types
HID_USAGE_CONST = 0x26    #    Usage ET Constant Force
HID_USAGE_RAMP  = 0x27    #    Usage ET Ramp
HID_USAGE_SQUR  = 0x30    #    Usage ET Square
HID_USAGE_SINE  = 0x31    #    Usage ET Sine
HID_USAGE_TRNG  = 0x32    #    Usage ET Triangle
HID_USAGE_STUP  = 0x33    #    Usage ET Sawtooth Up
HID_USAGE_STDN  = 0x34    #    Usage ET Sawtooth Down
HID_USAGE_SPRNG = 0x40    #    Usage ET Spring
HID_USAGE_DMPR  = 0x41    #    Usage ET Damper
HID_USAGE_INRT  = 0x42    #    Usage ET Inertia
HID_USAGE_FRIC  = 0x43    #    Usage ET Friction
