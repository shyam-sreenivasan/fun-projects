
def solve(arr):
    m = sm = float('-inf')
    for i in arr:
        if i > m:
            sm = m
            m = i
        elif i > sm and i != m:
            sm = i
        print(m, sm)
    return None if sm == float('-inf') else sm
        

if __name__ == "__main__":
    inputs = [
        [1,2,3],
        [1,3,2],
        [2,3,1],
        [2,1,3],
        [3,1,2],
        [3,2,1],
        [],
        [2, 3, 6, 6, 5]
    ]
    for arr in inputs:
        second_max = solve(arr)
        print(arr, second_max)
        print('=========================')