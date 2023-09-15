
def solve(denoms, target, curr_sum=0, choices=[], memo={}, index=0):

    if curr_sum == target:
        return True, choices
    
    if curr_sum > target or index > len(denoms):
        return False, None
    
    key = (index, curr_sum)
    if key in memo:
        return memo[key]

    #curr_sum still less than the target, so trying to add denoms
    results = []
    for i in denominations:
        found_with_denom, choices_with_denom = solve(denoms, target, curr_sum=curr_sum+i, choices=choices + [i],memo=memo, index=index+1)
        found_without_denom, choices_without_denom = solve(denoms, target, curr_sum=curr_sum, choices=choices,memo=memo, index=index+1)
        if found_with_denom:
            results.append((found_with_denom, choices_with_denom))

        if found_without_denom:
            results.append((found_without_denom, choices_without_denom))

    # find the result with the least coins
    if results:
        results = min(results, key=lambda x: len(x[1]))
        memo[key] = results
    else:
        memo[key] = (False, None)
    return memo[key]
           

if __name__ == "__main__":
    inputs = [
        {
            "d": [1,2,3], #denominations
            "t": 5 #target
        },
        {
            "d": [2,5,10],
            "t": 9
        },
        {
            "d": {1, 5, 10, 25},
            "t": 5
        },
    ]

    for test in inputs:
        denominations = test["d"]
        target = test["t"]
        found, choices = solve(denominations, target, curr_sum=0, choices=[], index=0)
        print(found, choices)
        break