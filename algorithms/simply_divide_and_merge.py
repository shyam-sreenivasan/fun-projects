def solve(arr):
    if len(arr) <= 1:
        print(arr)
        return arr
    
    mid = len(arr) // 2
    sub_a = solve(arr[:mid])
    sub_b = solve(arr[mid:])
    
    return sub_a + sub_b

if __name__ == '__main__':
    arr = [1,2,3,4]
    a = solve(arr)
    print("=======================")
    print(a)