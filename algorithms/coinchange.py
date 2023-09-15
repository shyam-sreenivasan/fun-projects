
def solve2(coins, target):
    dp = [[float('inf'), []]]*(target+1)
    dp[0] = [0, []]
    for coin in coins:
        for i in range(coin, target+1):
            if dp[i][0] < dp[i-coin][0] + 1:
                # dont add current coin
                dp[i] = [dp[i][0], dp[i][1]]
            else:
                dp[i] = [dp[i-coin][0] + 1, dp[i-coin][1] + [coin]]

    return dp[target][1]


def solve(denoms, target, curr_sum=0, choices=[], memo={}, index=0, dp_enabled=False):
    if curr_sum == target:
        return True, choices
    
    if curr_sum > target or index > len(denoms):
        return False, None
    
    key = (index, curr_sum)
    if dp_enabled and key in memo:
        return memo[key]

    #curr_sum still less than the target, so trying to add denoms
    results = []
    for i in denominations:
        found_with_denom, choices_with_denom = solve(denoms, target, curr_sum=curr_sum+i, choices=choices + [i],memo=memo, index=index+1, dp_enabled=dp_enabled)
        found_without_denom, choices_without_denom = solve(denoms, target, curr_sum=curr_sum, choices=choices,memo=memo, index=index+1, dp_enabled=dp_enabled)
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
        found, choices = solve(denominations, target, curr_sum=0, choices=[], index=0, memo={})
        print(f"Coins= {denominations}, target={target}")
        print("Recursion= ", choices)
        found, choices = solve(denominations, target, curr_sum=0, choices=[], index=0, memo={}, dp_enabled=True)
        print("Recursion with DP=", choices)
        print("Iterative DP=", solve2(denominations, target))
        print("==============")