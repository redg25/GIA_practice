import random
from typing import List
from collections import Counter


def number_speed_and_accuracy():
    ''' Return a list of 3 numbers compiling with the following rules:
        - Each number between 2 and 29
        - The difference between the 2 extremes is max 9
        - The minimum difference between any 2 numbers is 2
        - The difference between 2 numbers can't be the same'''
    def get_three_valid_numbers() -> List[int]:
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

    question = get_three_valid_numbers()
    answer = find_answer(question)
    return question, answer

def perceptual_speed():
    letters = {'a':[],
               'b':['d','p','q','g'],
               'c':['o'],
               'd':['b','p','q','g'],
               'e':[],
               'f':['k'],
               'g':['b','p','q','d'],
               'h':['k'],
               'i':['l','j'],
               'j':['i','l'],
               'k':['h'],
               'l':['i','j'],
               'm':['n'],
               'n':['m'],
               'o':['c'],
               'p':['b','g','q','d'],
               'q':['b','p','g','d'],
               'r':[],
               's':[],
               't':[],
               'u':['v'],
               'v':['w','u'],
               'w':['v'],
               'x':[],
               'y':[],
               'z':[]}

    def letter_choice():
        letter = random.choice(list(letters.keys()))
        choice_for_pair = list(letters.keys())
        for similar in letters[letter]:
            for n in range(9):
                choice_for_pair.append(similar)
        r = len(choice_for_pair)*8//10
        for n in range(r):
            choice_for_pair.append(letter)
        letter_pair = random.choice(choice_for_pair)
        return [letter,letter_pair]

    def get_question():
        up=[]
        down=[]
        while len(up)<4:
            new_pair = letter_choice()
            if new_pair[0] not in up and new_pair[1] not in down:
                up.append(new_pair[0])
                down.append(new_pair[1])

        if random.randbytes(1):
            up = [x.upper() for x in up]
        else:
            down = [x.upper() for x in down]
        return [up, down]

    def get_nb_of_pairs(lines:List[list]):
        score = 0
        up = lines[0]
        down = lines[1]
        for u,d in zip(up,down):
            if u.lower() == d.lower():
                score += 1
        return score

    question = get_question()
    all_letters = question[0]+ question[1]
    answer = get_nb_of_pairs(question)
    return all_letters, answer

def spatial_visualisation():

    choices = [(0,0),(0,90),(0,180),(0,270),(1,0),(1,90),(1,180),(1,270)]
    def get_non_matching_R():
        while True:
            pair = random.sample(choices,2)
            if pair[0][0] != pair[1][0]:
                return pair
    def get_matching_R():
        while True:
            pair = random.sample(choices,2)
            if pair[0][0] == pair[1][0] and pair[0]!=pair[1]:
                return pair

    result = random.randrange(3)
    questions = []
    if result == 0:
        while len(questions)<2:
            question = get_non_matching_R()
            if question not in questions:
                questions.append(question)
    elif result == 1:
        questions.append(get_matching_R())
        questions.append(get_non_matching_R())
        random.shuffle(questions)
    elif result == 2:
        while len(questions)<2:
            question = get_matching_R()
            if question not in questions:
                questions.append(question)
    return questions, result




# print(spatial_visualisation())
#
#
# stats=[]
# for n in range(1000):
#     stats.append(spatial_visualisation()[1])
#
# print(Counter(stats))