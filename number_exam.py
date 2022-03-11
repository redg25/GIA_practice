import random
from typing import List

def get_three_valid_numbers() -> List[int]:
    ''' Return a list of 3 numbers compiling with the following rules:
    - Each number between 2 and 29
    - The difference between the 2 extremes is max 9
    - The minimum difference between any 2 numbers is 2
    - The difference between 2 numbers can't be the same'''
    numbers = [0,0,0]
    while numbers[2]-numbers[0] > 9 \
            or numbers[2]-numbers[1]<2 \
            or numbers[1]-numbers[0]<2 \
            or numbers[2]-numbers[1] == numbers[1]-numbers[0]:
        numbers = sorted(random.sample(range(2,29),3))
    random.shuffle(numbers)
    return numbers


# Expect: The difference between 2 numbers of the list is not the same.
def find_answer(numbers:List[int]) -> int:
    sorted_numbers = sorted(numbers)
    if sorted_numbers[2]-sorted_numbers[1] > sorted_numbers[1]-sorted_numbers[0]:
        return sorted_numbers[2]
    else:
        return sorted_numbers[0]

def get_question_and_answer():
    question = get_three_valid_numbers()
    answer = find_answer(question)
    return question, answer


