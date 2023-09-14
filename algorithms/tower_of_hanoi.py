class Stack:
    def __init__(self,name, ls) -> None:
        self.name = name
        self.ls = ls

    def push(self, item):
        self.ls = [item] + self.ls

    def pop(self):
        return None if self.is_empty() else self.ls.pop(0)
    
    def length(self):
        return len(self.ls)
    
    def is_valid(self):
        return self.ls == sorted(self.ls)
    
    def is_empty(self):
        return self.length() == 0
    
    def get_state(self):
        if self.is_empty():
            return ''
        return f"{self.name}{''.join([str(c) for c in self.ls])}"
    
    def __repr__(self) -> str:
        return f"{self.name} => {self.ls}"


"""
In every step, there are 2 options.
    - store current state of the system. stacks + current pointer
    - pop the stack at the current pointer
        - try to push element to previous stack
        - try to push element to next stack
    - move to the next stack

"""
def solve(stacks, req_len, last_stack, curr_pointer=0, visited_states=[], depth=0):
    curr_stack = stacks[curr_pointer]
    all_state = "".join([s.get_state() for s in stacks]) + f"-{curr_pointer}"
    if(last_stack.is_valid() and last_stack.length() == req_len):
        return True, [all_state]
    
    if all_state in visited_states:
        return None, None

    if not curr_stack.is_valid():
        return None, None
    
    visited_states.append(all_state)

    can_push_to_prev_stack = False
    can_push_to_next_stack = False
    can_move_to_next_stack = False
    sub_results = []
    if curr_stack.length() > 0:
        top_value = curr_stack.pop()
        prev_stack = stacks[abs((curr_pointer-1)%len(stacks))]
        prev_stack.push(top_value)

        can_push_to_prev_stack, sub_states = solve(stacks, req_len, last_stack, curr_pointer=curr_pointer, visited_states=visited_states, depth=depth+1)
        sub_results.append((can_push_to_prev_stack, sub_states))

        prev_stack.pop()
        curr_stack.push(top_value)
        curr_stack.pop()
        next_stack = stacks[(curr_pointer+1)%len(stacks)]
        next_stack.push(top_value)
        
        can_push_to_next_stack, sub_states = solve(stacks, req_len, last_stack, curr_pointer=curr_pointer, visited_states=visited_states, depth=depth+1)

        sub_results.append((can_push_to_next_stack, sub_states))
        next_stack.pop()
        curr_stack.push(top_value)

    can_move_to_next_stack, sub_states = solve(stacks, req_len, last_stack, curr_pointer=(curr_pointer+1)%len(stacks), visited_states=visited_states, depth=depth+1)
    sub_results.append((can_move_to_next_stack, sub_states))

    min_sub = None
    min_len = None
    at_least_one_true = False

    for sr in sub_results:
        if sr[0]:
            at_least_one_true = True
            if min_len is None or len(sr[1]) < min_len:
                min_len = len(sr[1])
                min_sub = sr[1] 
    if min_sub:
        min_sub = [all_state] + min_sub  
    visited_states.pop() 
    return at_least_one_true, min_sub

    # just move
if __name__ == '__main__':
    stacks = [
    Stack("A", [1,2,3]),
    Stack("B", []),
    Stack("C", [])
]
    dest_stack = stacks[len(stacks) - 1]
    req_len = stacks[0].length()
    res, all_states = solve(stacks, req_len, dest_stack)
    states = []
    for s in all_states:
        sparts = s.split("-")
        if sparts[0] not in states:
            states.append(sparts[0])
            print(sparts[0])
