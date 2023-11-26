"""
Imagine you go to a shop that sells mangoes. You see the pricing that says
5 pcs - Rs 100
10 pcs - Rs 150
15 pcs - Rs 270
and so on.

How many mangoes should you buy and in what combination to maximize your profit margin ?

In this case, buy 5 pcs would give you 0 profit but buying 10 pcs would give you a profit margin
of Rs 50. Original price for 10 mangoes is Rs 200, but current price is Rs 50

If you bought 15 pcs at once, you have a profit margin of Rs 30.

But but...
If you bought the 15 pcs as 5pcs + 10 pcs , you buy the same for 250 Rs with a profit margin
of Rs 50. Hence in this case, this is by far the best outcome. 

Algorithm: 
lets consider the lowest value as 1 unit of purchase. That will tell us how many units are other
baskets and their orignal vs actual cost.

consider an input as the number of baskets you want to touch at least. Say 2, means i want to 
at least buy any 2 baskets or more.
Of those which has the best profit margin
There can be an upper range also
"""

# ALGORITHM_TYPE indicates whether the combination base case needs to be achieved based on total baskets collected or total quantity reached having collected 1 or more baskets.
# 0 means use total baskets. 1 means use total quantity reached
ALGORITHM_TYPE = 1
baskets_needed = 3
min_qty = 15
max_qty = 45

import pandas as pd
def process_combos_for_profit(basket_combos, unit_price, unit_value):
    result = []
    for c in basket_combos:
        total_price = 0
        original_price = 0
        total_qty = 0
        for item in c:
            total_price += item[2]
            original_price += int(int(item[1]) / int(unit_value) * int(unit_price))
            total_qty += int(item[1])
        result.append([c, total_price, total_qty, original_price, original_price - total_price])
    return result

class InvalidAlgorithmTypeException(Exception):
    pass

def is_base_case_reached(collected):
    global ALGORITHM_TYPE, baskets_needed, min_qty, max_qty
    if ALGORITHM_TYPE == 0:
        return len(collected) == baskets_needed
    
    if ALGORITHM_TYPE == 1:
        total = 0
        for c in collected:
            total += c[1]
        if total >= min_qty and total <= max_qty:
            return True
        return False
    raise InvalidAlgorithmTypeException

def solve(baskets, collected=None, index=0):
    if collected is None:
        collected = []

    if is_base_case_reached(collected):
        return [[x for x in collected]]
    
    if index >= len(baskets):
        return []
    # choosing current
    collected.append(baskets[index])
    with_current = solve(baskets, collected=collected, index=index+1)
    
    # not choosing current
    collected.pop()
    without_current = solve(baskets, collected=collected, index=index+1)

    collated = with_current + without_current
    return collated

def solve_iterative(baskets):
    stack = [(0, [])]
    result = []

    while stack:
        index, collected = stack.pop()

        if is_base_case_reached(collected):
            result.append([x for x in collected])
        elif index < len(baskets):
            # choosing current
            stack.append((index + 1, collected + [baskets[index]]))
            # not choosing current
            stack.append((index + 1, collected))

    return result

def solve_iterative_with_dp(baskets):
    stack = [(0, [])]
    dp = {}

    while stack:
        index, collected = stack.pop()

        if (index, tuple(collected)) in dp:
            continue

        if is_base_case_reached(collected):
            dp[(index, tuple(collected))] = [[x for x in collected]]
        elif index < len(baskets):
            # choosing current
            stack.append((index + 1, collected + [baskets[index]]))
            # not choosing current
            stack.append((index + 1, collected))
    result = []
    for _, value in dp.items():
        result.extend(value)
    return result

if __name__ == "__main__":
    baskets = (
        ("b1", 20, 400),
        ("b2", 5, 100),
        ("b3", 10, 150),
        ("b4", 15, 270) 
    )
    
    baskets = sorted(baskets, key=lambda x: x[1])
    unit_value = baskets[0][1]
    unit_price = baskets[0][2]    
    combos = solve_iterative_with_dp(baskets)
    result = process_combos_for_profit(combos, unit_price, unit_value)
    
    df = pd.DataFrame(result, columns=["baskets", "total_price", "total_quantity", "original_price", "profit_margin"])

    df = df.sort_values(by="profit_margin", ascending=False).reset_index(drop=True)
    print(df)
    print("-----------------------------------")