"""
if weight exceeds, return wt, val and sacks so far
if index exceeds, check if weight exceeded, if yes return wt, val, sacks so far

In each step, you can 2 do things.
    - pick an item
    - dont pick and item
"""
def solve(knapsack, max_wt, wt, val, sacks=[], index=0, memo={}):
    key = f"{index}{wt}"
    if index >= len(knapsack):
        return wt, val, sacks
    
    if key in memo:
        return memo[key]
    
    new_wt = wt + knapsack[index][0]
    new_val = val + knapsack[index][1]

    if new_wt > max_wt:
        return wt, val, sacks
    
    #pick curr item
    wt_with_pick, value_with_pick , sacks_with_pick = solve(knapsack, max_wt, wt=new_wt, val=new_val, sacks=sacks + [index], memo=memo, index=index+1)

    wt_without_pick, value_without_pick, sacks_without_pick = solve(knapsack, max_wt, wt=wt, val=val, sacks=sacks, memo=memo, index=index+1)

    with_pick = (wt_with_pick, value_with_pick, sacks_with_pick)

    without_pick = (wt_without_pick, value_without_pick, sacks_without_pick)
    
    memo[key] = with_pick if value_with_pick > value_without_pick else without_pick
    return memo[key]
        

if __name__ == "__main__":
    items = [
        [10, 60],
        [20, 100],
        [30, 120]
    ]
    max_weight = 50
    weight, value, sacks = solve(items, max_weight, 0, 0)
    print("Best Value=", value)
    print("Max Possible weight", weight)
    print("Items=", sacks)