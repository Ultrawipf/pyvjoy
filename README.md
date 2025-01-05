Forked from [tidzo/pyvjoy](https://github.com/tidzo/pyvjoy) to support FFB callbacks.

Note: FFB support requires a 2.2.x version for the effect block index to work properly.
The original vJoy project on vjoystick.sourceforge is not being updated anymore and does not support FFB properly. 

It is recommended to use a fork like [BrunnerInnovation/vJoy](https://github.com/BrunnerInnovation/vJoy).

The interface dll from this fork is being used for FFB.

With this library you can easily set Axis and Button values on any vJoy device and receive force feedback effect data.
Low-level bindings are provided in pyvjoy._sdk as well as a (hopefully) slightly more 'Pythonic' API in the pyvjoy.VJoyDevice() object.

The usage of non FFB functions is identical to the original pyvJoy project.

## Standard pyvjoy usage:
```python
import pyvjoy

#Pythonic API, item-at-a-time

j = pyvjoy.VJoyDevice(1)

#turn button number 15 on
j.set_button(15,1)

#turn button 15 off again
j.set_button(15,0)

#Set X axis to fully left
j.set_axis(pyvjoy.HID_USAGE_X, 0x1)

#Set X axis to fully right
j.set_axis(pyvjoy.HID_USAGE_X, 0x8000)

#Also implemented:
j.reset()
j.reset_buttons()
j.reset_povs()

#The 'efficient' method as described in vJoy's docs - set multiple values at once

j.data.lButtons = 19 # buttons number 1,2 and 5 (1+2+16)
j.data.wAxisX = 0x2000 
j.data.wAxisY= 0x7500

#send data to vJoy device
j.update()
```
## Simple FFB example with callbacks: 
```python
import pyvjoy
import time

j = pyvjoy.VJoyDevice(1)
# FFB functions

# Use effect manager helper to simplify effect handling
# idx (index in effect list) is blockindex-1 because blockindex always starts with 1.
# Effect events can be received using the separate callback functions or by overriding update_packet_cb, update_effect_dict_cb or __ffb_cb

class EffMan(pyvjoy.FFB_Effect_Manager):
	
	def update_ctrl_cb(self,ctrl): # 1 = enable, 2 = disable
		print("Control",ctrl)
	
	def update_constant_cb(self,data,idx): # Constant force magnitude
		print("CF",data["Magnitude"])

	# Also implemented (Function dummys from FFB_Effect_Manager class)
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

	def update_ramp_cb(self,data,idx):
		"""Set ramp callback"""
		return

	def update_effect_dict_cb(self,packetdict,idx):
		return


if j.ffb_supported(): # Only if FFB is actually enabled in device and driver
	effectManager1 = EffMan()
	effectManager1.ffb_register_callback(j)
time.sleep(100)
print("End")
```
## Low level minimal FFB example without creating the FFB_Effect_Manager:
```python
import pyvjoy
import time

j = pyvjoy.VJoyDevice(1)

def ffbcb(data,reptype):
	packetdict,ebi = pyvjoy.FFB_Effect_Manager.ffb_packet_to_dict(data,reptype)
	print(packetdict,ebi)

j.ffb_register_callback(ffbcb)
time.sleep(100)
print("End")
```


