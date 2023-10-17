
from functools import reduce
def equals(a, b):
    if a is not None and b is not None:
        return a if len(a) == len(b) else None
    return None

"""
Given a characters array tasks, representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.

However, there is a non-negative integer n that represents the cooldown period between two same tasks (the same letter in the array), that is that there must be at least n units of time between any two same tasks.

Return the least number of units of times that the CPU will take to finish all the given tasks.


Example 1:

Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
Explanation: 
A -> B -> idle -> A -> B -> idle -> A -> B
There is at least 2 units of time between any two same tasks.
Example 2:

Input: tasks = ["A","A","A","B","B","B"], n = 0
Output: 6
Explanation: On this case any permutation of size 6 would work since n = 0.
["A","A","A","B","B","B"]
["A","B","A","B","A","B"]
["B","B","B","A","A","A"]
...
And so on.
Example 3:

Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2
Output: 16
Explanation: 
One possible solution is
A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A
"""

def cpu_min_time(tasks, idle_time):
    from collections import OrderedDict
    # sort the tasks by order of max same tasks.
    # iterate through each task.
    # check if you can proccess it
        # peek the task in the queue. it its not eligible for processing
        # check if current task is eligible, if not
        # add to queue and mark an idle count
        # otherwise process the current task
    
    sorted_task_group = {}
    for t in tasks:
        if t not in sorted_task_group:
            sorted_task_group[t] = 0
        sorted_task_group[t] += 1
    sorted_task_group = OrderedDict(sorted(sorted_task_group.items(), key=lambda x : x[1], reverse=True))
    print(sorted_task_group)

    # ==============================================
    sorted_tasks = []
    for key, value in sorted_task_group.items():
        sub_tasks = [key]*value
        sorted_tasks.extend(sub_tasks)
    print(sorted_tasks)

    #==================================================

    # task_idle_time = {}
    # for key, value in sorted_task_group:
    #     task_idle_time[key] = 0
    # ============================================
    pointer = 0
    task_cycle_map = {}
    TASK_COMPLETED = -1
    cycle = 0
    total_tasks = len(sorted_tasks)
    completed_task_order = []
    while pointer < total_tasks:
        print(f"Cycle: {cycle}, tasks {sorted_tasks}", pointer)
        
        curr_task = sorted_tasks[pointer]
        if curr_task == TASK_COMPLETED:
            # print("Task completed", pointer)
            pointer += 1
            continue
        
        def process_current_task(tasks, curr_task, pointer, cycle, task_cycle_map, completed_task_order):
            last_cycle = task_cycle_map.get(curr_task)
            # print(curr_task, pointer, last_cycle, cycle)
            processed = False
            if last_cycle is None or (cycle-last_cycle) > idle_time:
                completed_task_order.append((tasks[pointer], pointer))
                task_cycle_map[curr_task] = cycle
                tasks[pointer] = -1
                processed = True
            return processed
        
        processed = process_current_task(sorted_tasks, curr_task, pointer, cycle, task_cycle_map, completed_task_order)
        
        if processed:
            cycle += 1
            pointer += 1
            continue
        
        # print("Not processed. checking if pointer in last -1 ")
        if pointer == len(sorted_tasks) - 1:
            cycle += 1
            continue

        j = pointer + 1
        processed = False
        while j < total_tasks:
            # print("j is", j)
            if sorted_tasks[j] == TASK_COMPLETED:
                # print("Task completed", j)
                j += 1
                continue
            
            processed = process_current_task(sorted_tasks, sorted_tasks[j], j, cycle, task_cycle_map, completed_task_order)
            # print(".................")
            # print(j, processed, pointer, cycle, curr_task, sorted_tasks)
            if processed:
                cycle += 1
                break
            j += 1

        if not processed:
            cycle += 1
            completed_task_order.append("IDLE")

    return cycle, completed_task_order

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