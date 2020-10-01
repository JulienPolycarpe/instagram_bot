import logging
import threading
import time

def thread_function(name):
	logging.info("Thread %s: starting", name)
	time.sleep(5)
	logging.info("Thread %s: finishing", name)

def thread_function2(name):
	logging.info("Thread %s: starting", name)
	time.sleep(2)
	logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt="[%D] %H:%M:%S")

	logging.info("Main    : before creating thread")
	x = threading.Thread(target=thread_function, args=("x",))
	y = threading.Thread(target=thread_function2, args=("y",))
	logging.info("Main    : before running thread")
	x.start()
	y.start()
	logging.info("Main    : wait for the thread to finish")
	# x.join()
	logging.info("Main    : all done")
	a = 70 - 60 if (70 - 60) >= 0 else 0
	print(a)
