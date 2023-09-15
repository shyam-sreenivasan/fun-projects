import sys
def merge(a, b):
    c = []
    i=0
    j=0
    # compare and append at least one of array is finished
    while i < len(a) and j < len(b):
            if a[i] < b[j]:
                c.append(a[i])
                i = i+1
            else:
                c.append(b[j])
                j = j+1

    
    # add the remaining extra elements
    while i < len(a):
         c.append(a[i])
         i += 1

    while j < len(b):
         c.append(b[j])
         j += 1

    return c

def solve(arr, start, end, depth=0):
    if start >= end:
        return [arr[start]]
    
    mid = (start + end) // 2
    sub_a = solve(arr, start=start, end=mid, depth=depth+1)
    sub_b = solve(arr, start=mid+1, end=end, depth=depth+1)
    
    return merge(sub_a, sub_b)

if __name__ == '__main__':
    arr = [10, 5, 3, 4, 2, 7]
    a = solve(arr, 0, len(arr)-1)
    print(a)