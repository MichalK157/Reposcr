
import rbqscripts as rbq
import threading
import time

def main():
	state=False
#
# Init obj
	print("INIT")
	re = rbq.Uniwersalreceiver()
	thr = threading.Thread(target=re.receive,daemon=True)
	thr.start()
	#thr.join()

###
	if state == False:
		state=True
		print("loop Start")
	while True:
		while re.g_return:
			print('I will make sommething')
			time.sleep(1)
			o_send=rbq.UniwersalSend()
			o_send.send('Pass')
			re.g_return=False
		pass

main()
