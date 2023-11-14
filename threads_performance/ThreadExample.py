import threading
import time
import sys
import json


def count(tid):
	counter = 0
	for i in range(MAX_ITERATIONS):
		counter += 1
	# print("Thread {} done. Counter= {}".format(tid, counter))

if __name__ == "__main__":
	result = []
	run_inputs = json.load(open('thread_inputs.json', 'r'))
	for data in run_inputs['runs']:
		start = time.time()
		TOTAL_THREADS = data["t"]
		MAX_ITERATIONS = data["i"]
		threads = []
		for i in range(TOTAL_THREADS):
			t = threading.Thread(target=count, args=(i,))
			t.start()
			threads.append(t)

		for t in threads:
			t.join()
		end = time.time()
		print("All threads for t={}, i={} completed in {} ms".format(TOTAL_THREADS, MAX_ITERATIONS, round(end - start,3)*1000))
		result.append({
			"threads": TOTAL_THREADS,
			"iterations": MAX_ITERATIONS,
			"time_taken": f"{round(end - start,3)*1000} ms"
			})
	print(result)