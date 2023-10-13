
from functools import reduce
def equals(a, b):
    if a is not None and b is not None:
        return a if len(a) == len(b) else None
    return None

def island(arr):
    visited = {}
    rows = len(arr)
    columns = len(arr[0])

    def find(arr, rows, columns, curr_row, curr_col, visited, lands):
        if curr_row < 0 or curr_row >= rows or curr_col < 0 or curr_col >= columns:
            # gone outside the matrix
            return 0 
        
        if (curr_row, curr_col) in visited:
            return 0
                
        visited[(curr_row, curr_col)] = 1
        if int(arr[curr_row][curr_col]) == 0:
            return 0
        # go right
        right = find(arr, rows, columns, curr_row, curr_col+1, visited, lands)
        left = find(arr, rows, columns, curr_row, curr_col-1, visited, lands)
        # go down
        up = find(arr, rows, columns, curr_row-1, curr_col, visited, lands)
        down = find(arr, rows, columns, curr_row+1, curr_col, visited, lands)
        lands.append((curr_row, curr_col))
        return left + right + up + down + 1
    
    count = 0
    islands_collection = []
    for i in range(rows):
        for j in range(columns):
            lands = []
            if int(arr[i][j]) != 0 and (i,j) not in visited:
                find(arr, rows, columns, i, j, visited=visited, lands=lands)
                count += 1
                islands_collection.append(lands)
        
    return count, islands_collection
        

# given an array whose length is always even, split them into all combinations of two groups.
def two_groups(arr, group_size, index=0, group_one=[], group_two=[]):
    if len(group_one) == group_size and len(group_two) == group_size:
        print(group_one, group_two)
        return
    
    if index >= len(arr):
        return
    
    if len(group_one) < group_size:
        group_one.append(arr[index])
        two_groups(arr, index=index+1, group_one=group_one, group_two=group_two, group_size=group_size)
        group_one.pop()

    if len(group_two) < group_size:
        group_two.append(arr[index])
        two_groups(arr, index=index+1, group_one=group_one, group_two=group_two, group_size=group_size)
        group_two.pop()

def n_groups(arr, n):
    def n_groups_inner(arr, n, group_size, index=0, groups=[]):
        res = reduce(equals, groups)
        if res is not None and len(res) == group_size:
            print(groups)
            return
        
        if index >= len(arr):
            return
        
        for group in groups:
            if len(group) < group_size:
                group.append(arr[index])
                n_groups_inner(arr, n, group_size, index=index+1, groups=groups)
                group.pop()

    groups = []
    for i in range(n):
        groups.append([])
    n_groups_inner(arr, n, len(arr)/n, index=0, groups=groups)


def can_contruct_from_vocabulary(word, vocabs, stripped_word):
    if stripped_word == "":
        return True
    
    for vocab in vocabs:
        if word.startswith(vocab):
            stripped_word = stripped_word[len(vocab):]
            can_construct = can_contruct_from_vocabulary(word, vocabs, stripped_word)
            if can_construct:
                return True
    
    return False

def min_processing_timen(processing_times, tasks):
    group_size = len(tasks) // len(processing_times)
    # the idea is to get the combination of every group with every processor and finally
    # get the one with the minimum time across, (max of any one processor group).
    # meaning that it will at least take that much time, but overall considering other arrangements
    # its fastest.

    def minimum_processing_time(processing_times, tasks, group_size, index=0, task_groups=[]):
        pass

# leetcode contest 366, problem 2
# this solution is good only for 2 processors, need to extend for N processors and then optimize it.
def min_processing_time(processors_time, tasks):
    processors_time = sorted(processors_time)
    def minimum_processing_time(processors_time, tasks, index=0, task_group_one=[], task_group_two=[]):
        # create 2 groups where in one group you add a task and in the other you dont and recursively do it.
        group_size = len(tasks) // len(processors_time)
        group_one_size = len(task_group_one)
        group_two_size = len(task_group_two)
        if group_one_size == group_size and group_two_size == group_size:
            group_one_max = max(task_group_one)
            group_two_max = max(task_group_two)

            group_one_max_with_pr1 = group_one_max + processors_time[0]
            group_two_max_with_pr2 = group_two_max + processors_time[1]

            res1 = max(group_one_max_with_pr1, group_two_max_with_pr2)

            group_one_max_with_pr2 = group_one_max + processors_time[1]
            group_two_max_with_pr1 = group_two_max + processors_time[0]

            res2 = max(group_one_max_with_pr2, group_two_max_with_pr1)

            # if task_group_two == [8, 7, 4, 5] or task_group_one == [8, 7, 4, 5]:
            #     print(task_group_one, task_group_two)
            #     print(group_one_max, group_two_max)
            #     print(group_one_max_with_pr1, group_two_max_with_pr2)
            #     print(group_one_max_with_pr2, group_two_max_with_pr1)
            #     print(res1, res2)


            return min(res1, res2)        
        
        if index >= len(tasks):
            return
        
        # add current element either to group one or group two
        res1 = None
        if len(task_group_two) < group_size:
            task_group_one.append(tasks[index])
            res1 = minimum_processing_time(processors_time, tasks, index=index+1, task_group_one=task_group_one, task_group_two=task_group_two)
            task_group_one.pop()

        res2 = None
        if len(task_group_two) < group_size:
            task_group_two.append(tasks[index])
            res2 = minimum_processing_time(processors_time, tasks, index=index+1, task_group_one=task_group_one, task_group_two=task_group_two)
            task_group_two.pop()

        if res1 and res2:
            return min(res1, res2)
        
        if res1 or res2:
            return res1 or res2
        
        return None
    
    ret = minimum_processing_time(processors_time, tasks)
    return ret
# leetcode contest 366, problem 1
# given 2 integers n and m, find num1 - num2, where num1 is all elements not divisble by m and 
# num2 is all numbers divisible by m, in the range 1...n
def divisible_nondivisible_sum_diff(n, m):
    sum_till_n = n*(n+1) // 2
    num2 = sum(i for i in range(1, n+1) if i % m == 0)
    num1 = sum_till_n - num2
    return num1 - num2

def split_string_with_binary_patterns(s, total_spaces):
    def has_ones_equal_to(bstring, total_spaces):
        count = 0
        for i in bstring:
            if count > total_spaces:
                return False
            if i == "1":
                count += 1

        return count == total_spaces
    
    max_spaces = len(s) - 1
    total_combinations = 2**max_spaces
    patterns = []
    for i in range(total_combinations):
        pattern = str(bin(i))[2:]
        pattern = "0"*(len(s) - len(pattern)) + pattern
        if has_ones_equal_to(pattern, total_spaces):
            patterns.append(pattern)
    
    gen_strings = []
    for pat in patterns:
        gen_string = s
        for i, c in enumerate(pat):
            if c == "1":
                gen_string = gen_string[:i] + " " + gen_string[i:]
                gen_strings.append(gen_string)
    return gen_strings

def split_string_iterative(s, total_spaces):
    q = [
        (s[0], 0)
    ]
    index = 1
    n = len(s)
    while index < len(s):
        q_size = len(q)
        i = 0
        while i < q_size:
            subs, spaces_used = q.pop(0) # item is a tuple that has substring and space used. ("1", 0) or ("12 3", 1)
            if spaces_used < total_spaces:
                new_subs = f"{subs} {s[index]}"
                q.append((new_subs, spaces_used + 1))

            q.append((f"{subs}{s[index]}", spaces_used))
            i += 1
        index += 1

    return [item[0] for item in q if item[1] == total_spaces]

# given n spaces, insert the spaces in all possible ways to spit the give string into multiple string
def split_string(s, total_spaces):

    # function call is below the function definition. Look at the bottom.
    def split(s, subs, index=1, space_used=0, total_spaces=1):
        # if total spaces you can insert can always be len(s) - 1. So this condition to check invalid inputs
        if total_spaces >= len(s):
            print("Invalid total spaces")
            return 
        
        # whenver i seen all numbers in the string and included in the substring
        if index >= len(s):
            # and also making sure all spaces have been used.
            # since its possible to visit all elements and failed to have used the spaces also
            if space_used == total_spaces:
                print(subs)
            return
        
        # insert a space after the current substring followed but the 
        # element in the current index if enough spaces haven;t been used
        if space_used < total_spaces:
            split(s, subs=f"{subs} {s[index]}",index=index+1, space_used=space_used+1, total_spaces=total_spaces)

        # dont insert
        # add the current element to the substring without space.
        split(s, subs=f"{subs}{s[index]}", index=index+1, space_used=space_used, total_spaces=total_spaces)

    # calling the split method with first element as the substring 
    # (since i dont have to insert a space before that but only after that)
    # i have total spaces and spaces_used. index=1 pointing at the second element
    split(s, subs=s[0], index=1, space_used=0, total_spaces=total_spaces)


def permutation(s, subs=""):
    if len(subs) == len(s):
        print(subs)
        return
    
    for c in s:
        permutation(s, subs=subs+c)
        
# removing duplicates from a sorted array
def remove_duplicates(a):
    i = 0
    j = i + 1
    while i < len(a) - 1:
        # print(i, j, len(a), a)
        if a[i] == a[i+1]:
            del a[i + 1]
        else:
            i += 1

    print(a)

def grid_traveller_recursive(m,n):
    total_ways = 0
    def traverse(i, j, m, n):
        if (i,j) == (m-1, n-1):
            return 1
        if i >= m or j >= n:
            return 0
    
        return traverse(i, j+1, m, n) + traverse(i+1, j, m, n)
    
    return traverse(0,0,m,n)
        
def grid_traveller_iterative(m, n):
    q = []
    q.append((0,0))
    target = (m-1, n-1)
    total_ways = 0
    while len(q) != 0:
        pos = q.pop(0)
        if pos == target:
            total_ways += 1
            
        if pos[0] < m - 1:
            down = (pos[0]+1, pos[1])
            q.append(down)

        if pos[1] < n - 1:
            right = (pos[0], pos[1]+1)
            q.append(right)
    return total_ways

def create_subsets_iterative(a):
    q = []
    q.append([])
    arr_len = len(a)
    for i in range(arr_len):
        # dequeue from the from , append the current element and add both back to queue
        q_len = len(q)
        j = 0
        while j < q_len:
            subset = q.pop(0)
            new_subset = subset + [a[i]]
            q.append(subset)
            q.append(new_subset)
            j += 1
    return q

def create_consecutive_subsets_iterative(a):
    q = []
    q.append([])
    arr_len = len(a)
    for i in range(arr_len):
        q_len = len(q)
        j = 0
        while j < q_len:
            subset = q.pop(0)
            # making sure the current index and the index of the last element of the subset is consecutive
            # so that it can be added to the current subset
            if subset == [] or (i - a.index(subset[-1])) == 1:
                new_subset = subset + [a[i]]
                q.append(new_subset)
            q.append(subset)
            j += 1
    return q
    


# arr = [1, 1, 2, 2, 2]

if __name__ == "__main__":
    functions = [
        {
            "name": "remove_duplicates",
            "run": False,
            "tests": [
                {
                    "ar": [],
                    "kw": {"a": [1,1,2,2,2]}
                }
            ]
        },
        {
            "name": "create_subsets_iterative",
            "run": False,
            "tests": [
                {
                    "ar": [],
                    "kw": {"a": [1,2,5]}
                }
            ]
        },
        {
            "name": "create_consecutive_subsets_iterative",
            "run": False,
            "tests": [
                {
                    "ar": [],
                    "kw": {"a": [1,2,5]}
                }
            ]
        }, 
        {
            "name": "grid_traveller_iterative",
            "run": False,
            "tests": [
                {
                    "ar": (2,2),
                    
                },
                {
                    "ar": (2,3)
                },
                {
                    "ar": (3,3),
                },
                {
                    "ar": (3,4)
                }
            ],
            "res_msg": "Total ways to reach the target="
        },
        {
            "name": "grid_traveller_recursive",
            "run": False,
            "tests": [
                {
                    "ar": (2,2),
                },
                {
                    "ar": (2,3)
                },
                {
                    "ar": (3,3)
                },
                {
                    "ar": (3,4)
                }
            ],
            "res_msg": "Total ways to reach the target="
        },
        {
            "name": "permutation",
            "run": False,
            "tests": [{
                "kw": {"s": "ab"}
            }]
        },
        {
            "name": "split_string",
            "run": False,
            "tests": [
                {
                    "kw": {"s": "1234", "total_spaces": 2}
                }
            ]
        },
        {
            "name": "split_string_iterative",
            "run": False,
            "tests": [
                {
                    "kw": {"s": "1234", "total_spaces": 2}
                }
            ]
        },
        {
            "name": "can_contruct_from_vocabulary",
            "run": False,
            "tests": [
                {
                    "kw": {
                        "word": "xyz",
                        "vocabs": ["abc", "cde", "d", "de"],
                        "stripped_word": "xyz"
                    }
                },
                {
                    "kw": {
                        "word": "abcde",
                        "vocabs": ["abc", "cde", "d", "de"],
                        "stripped_word": "abcde"
                    }
                },
                {
                    "kw": {
                        "word": "cdedde",
                        "vocabs": ["abc", "cde", "d", "de"],
                        "stripped_word": "cdedde"
                    }
                }
            ]
        },
        {
            "name": "divisible_nondivisible_sum_diff",
            "run": False,
            "tests": [
                {
                    "ar": (10,3)
                },
                {
                    "ar": (5,6)
                },
                {
                    "ar": (5,1)
                }
            ]
        },
        {
            "name": "min_processing_time",
            "run": False,
            "tests": [
                {
                    "ar": ([8,10], [2,2,3,1,8,7,4,5])
                },
                {
                    "ar": ([10,20], [2,3,1,2,5,8,4,3])
                }
            ]
        },
        {
            "name": "split_string_with_binary_patterns",
            "run": False,
            "tests": [
                {
                    "ar": ("123", 1)
                }
            ]
        },
        {
            "name": "two_groups",
            "run": False,
            "tests": [
                {
                    "ar": ([1,2,3,4], 2)
                }
            ]
        },
        {
            "name": "n_groups",
            "run": False,
            "tests": [
                {
                    "ar": ([1,2,3,4], 2)
                },
                {
                    "ar": ([1,2,3,4,5,6], 3)
                }
            ]
        },
        {
            "name": "island",
            "run": True,
            "tests": [
                {
                    "kw": {"arr": [[1]]}
                },
                {
                    "kw": {"arr": [[1, 0], [1,1]]}
                },
                {
                    "kw": {"arr": [[1, 0], [0, 1]]}
                },
                {
                    "kw": {"arr": [[1, 1], [1, 1]]}
                },
                {
                    "kw": {"arr": [[1, 0, 1], [1, 0, 1], [1, 0, 1]]}
                },
                {
                    "kw": {"arr": [[1, 1, 1], [0, 0, 0], [1, 1, 1]]}
                },
                {
                    "kw": {"arr": [[1, 1, 1, 1], [0,0,1,0], [0,0,0,0], [1,1,1,1]]}
                },
                {
                    "kw": {"arr": [[1,1,1,1,0],[1,1,0,1,0],[1,1,0,0,0],[0,0,0,0,0]]}
                },
                {
                    "kw": {"arr": [[1,1,1],[0,1,0],[1,1,1]]}
                },
                {
                    "kw": {
                        "arr": [["1","1","1","1","1","0","1","1","1","1"],["1","0","1","0","1","1","1","1","1","1"],["0","1","1","1","0","1","1","1","1","1"],["1","1","0","1","1","0","0","0","0","1"],["1","0","1","0","1","0","0","1","0","1"],["1","0","0","1","1","1","0","1","0","0"],["0","0","1","0","0","1","1","1","1","0"],["1","0","1","1","1","0","0","1","1","1"],["1","1","1","1","1","1","1","1","0","1"],["1","0","1","1","1","1","1","1","1","0"]]
                    }
                }
            ]
        }

    ]

    lc = locals()
    for f in functions:
        # check if run is set to True
        if not ("run" in f and f["run"]):
            continue

        func = lc.get(f['name'])
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