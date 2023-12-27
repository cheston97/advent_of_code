import math
from collections import deque

# Test input value is 13
INPUT = 'input.txt'

lines = [line.strip() for line in open(INPUT).readlines()]

def strip_and_remove_empty(nums: [str]):
    return [x.strip() for x in nums if x.strip()]

def has_duplicates(nums: [str]):
    return len(set(nums)) < len(nums)

def score_for_num_winning(num: int):
    return math.pow(2, num_winning - 1)

total_score = 0

num_winning_per_card = []
cards_to_play = deque()

for line_num, line in enumerate(lines):
    _, numbers = line.split(': ')
    winning_nums_str, my_nums_str = numbers.split(' | ')
    winning_nums = strip_and_remove_empty(winning_nums_str.split(' '))
    my_nums = strip_and_remove_empty(my_nums_str.split(' '))
    
    if has_duplicates(winning_nums):
        print('Winning nums has dupes')
    if has_duplicates(my_nums):
        print('My nums has dupes')
    
    num_winning = len(set(winning_nums).intersection(set(my_nums)))
    num_winning_per_card.append(num_winning)
    cards_to_play.append(line_num)

total_num_cards_played = 0
while len(cards_to_play) > 0:
    card_to_play = cards_to_play.popleft()
    if card_to_play >= len(num_winning_per_card):
        continue
    total_num_cards_played += 1
    card_num_winning = num_winning_per_card[card_to_play]
    for x in range(card_to_play + 1, card_to_play + 1 + card_num_winning):
        cards_to_play.append(x)

print(total_num_cards_played)
