"""
Problem link - https://www.hackerrank.com/challenges/candies/problem?isFullScreen=true&h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=dynamic-programming
"""
def solve3(scores, candies, index=1, memo={}):
    if index >= len(scores):
        return candies
    
    key = f"{index}{candies[index-1]}{candies[index]}"
    
    if key in memo:
        return memo[key]
    
    candies = solve3(scores, candies, index=index+1)
    curr_score = scores[index]
    curr_candies = candies[index]
    prev_score = scores[index-1]
    prev_candies = candies[index-1]
    print(index, prev_score, curr_score, prev_candies, curr_candies)
    if curr_score > prev_score:
        if curr_candies <= prev_candies:
            candies[index] = candies[index] + 1
            candies = solve3(scores, candies,index=index+1)
    
    if prev_score > curr_score:
        if prev_candies <= curr_candies:
            candies[index-1] = candies[index-1] + 1
            candies = solve3(scores, candies, index)

    memo[key] = candies
    return  memo[key]

def solve2(scores, candies):
    index = 0
    counter = 0

    while True:
        counter += 1
        if index >= len(scores):
            break
        candies[index] = candies[index] + 1
        curr_score_greater = False if index < 1 else scores[index-1] < scores[index]

        prev_score_greater = False if index < 1 else scores[index-1] > scores[index]
        if prev_score_greater:
            if candies[index - 1] <= candies[index]:
                candies[index] -= 1
                index = index - 1
                continue

        if curr_score_greater:
            if candies[index] <= candies[index-1]:
                candies[index - 1] = candies[index - 1] - 1 
                index = index - 1
                continue

        index += 1
    return sum(candies)
        
def solve(scores, min_candies, candies=[], index=0):

    if len(candies) == len(scores):
        return sum(candies)
    
    curr_candies = min_candies
    curr_score_greater = False if index < 1 else scores[index-1] < scores[index]

    if curr_score_greater:
        curr_candies = candies[index-1] + min_candies

    prev_score_greater = False if index < 1 else scores[index-1] > scores[index]

    if prev_score_greater:
        if candies[index - 1] <= candies[index]:
            candies.pop()
            return -1

    candies.append(curr_candies)
    
    while True:
        candies[index] = curr_candies
        # print('curr candies is', curr_candies)
        # print("Here candies", candies, index)
        if prev_score_greater:
            if candies[index - 1] <= candies[index]:
                candies.pop()
                return -1
            
        candies_given = solve(scores, min_candies, candies=candies, index=index+1)
        if candies_given >= 0:
            return candies_given
        
        curr_candies += 1


    
if __name__ == "__main__":
    scores = [2,4,2,6,1,7,8,9,2,1]
    # scores = [3, 2, 1]
    candies = []
    min_candies = 1
    # print(solve(scores, min_candies, candies, 0))
    print(scores)
    print("i","s", "S", "c", "C")
    candies = solve3(scores, [1]*len(scores))
    print(candies)
    print(sum(candies))
