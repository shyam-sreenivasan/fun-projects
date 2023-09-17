
def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp
    
def arrange(arr, start, pivot_index):
    i = start
    j = i + 1
    while j < pivot_index:
        if arr[i] > arr[pivot_index]:
            swap(arr, i, j)
        else:
            i += 1
        j += 1
    swap(arr, i, pivot_index)
    return i
    
def solve(arr, start, pivot_index):
    if start >= pivot_index:
        return arr
    new_pos = arrange(arr, start, pivot_index)
    arr = solve(arr, start, pivot_index=new_pos-1)
    arr = solve(arr, start=new_pos+1,pivot_index=pivot_index)
    return arr
    

if __name__ == "__main__":
    arr = [4,3,2,1]
    print(solve(arr,0, 3))