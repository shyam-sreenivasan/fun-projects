import subprocess
import json
import sys

if __name__ == '__main__':
	data = json.load(open('thread_inputs.json', 'r'))
	results = []
	for row in data["runs"]:
		num_t = row['t']
		num_i = row['i']
		java = ["java", "ThreadExample", str(num_t), str(num_i)]
		c = ["./pthread", str(num_t), str(num_i)]
		if sys.argv[1] == "java":
			result = subprocess.run(java, capture_output=True)
		elif sys.argv[1] == "c":
			result = subprocess.run(c, capture_output=True)
		else:
			sys.exit(1)
		results.append({
			"threads": num_t,
			"iterations": num_i,
			"time_in_ms": result.stdout.decode('utf-8')[:-1]
			})
	print(results)