
import rbqscripts as rbq
import threading
from getkey import getkey, keys

def main():
	state=False
#
# Init obj
	print("INIT")
	re = rbq.Uniwersalreceiver()
	thr = threading.Thread(target=re.receive,daemon=True)
	thr.start()
	#thr.join()

##

	if state == False:
		state=True
		print("loop Start")
	while True:
		while re.g_return:
			re.g_return=False
		key = getkey()
		if key == keys.ESC:
			break
		elif key == keys.ENTER:
			print("ENTER")
			o_send=rbq.UniwersalSend()
			o_send.send('run')

		pass

main()
