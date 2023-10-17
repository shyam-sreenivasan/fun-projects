
import json
import pathlib
import os
import solutions


if __name__ == "__main__":
    parent_folder = str(pathlib.Path(__file__).parent.resolve())
    functions = json.load(open(os.path.join(parent_folder,"functions.json"), 'r'))
    for f in functions:
        # check if run is set to True
        if not ("run" in f and f["run"]):
            continue

        func = getattr(solutions, f["name"])
        # checking if function is defined
        if not func:
            print(f"{f['name']}() function is not defined")
            continue

        print(f">>> Running function => {f['name']}()")
        for i in range(len(f['tests'])):
            t = f['tests'][i]
            if t.get('skip'):
                continue
            print(f">> \nTest case: {t}")
            ret_val = func(*t.get('ar',[]), **t.get("kw", {}))
            print("-------------------------------------------")
            print(f"Function returned: ", f.get("res_msg", ""), ret_val)
            print("-------------------------------------------")
            print(f"TEST CASE {i} completed for {f['name']}()")
        print("===========================")