import time
import pyvjoy


j = pyvjoy.VJoyDevice(1)

class EffMan(pyvjoy.FFB_Effect_Manager):
	 
	def update_effect_dict_cb(self,packetdict,idx):
		"""Called after every ffb update with parsed dict by update_packet_cb"""	
		self.print_effect(self.effects[idx]) # Print current internal effect state
	
	def update_ctrl_cb(self,ctrl):
		print("Device control",ctrl)

	def update_effect_op_cb(self,enabled,idx):
		print(f"Effect {idx} state change {enabled}")
	
	def update_effect_cb(self,data,idx):
		print("data",data)

	def update_condition_cb(self,data,idx):
		print("cond",data)

	def update_constant_cb(self,data,idx):
		print("CF",data["Magnitude"])

effectManager1 = EffMan()


if j.ffb_supported():
	print("J1 supports ffb")
	effectManager1.ffb_register_callback(j)


time.sleep(100)
print("End")