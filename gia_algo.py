import random
from typing import List
from collections import Counter
import csv


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
        choice_for_pair = list(letters.keys()) + letters[letter] * 9
        r = len(choice_for_pair) * 8 // 10
        choice_for_pair += [letter] * r
        letter_pair = random.choice(choice_for_pair)
        return [letter, letter_pair]

    def get_question():
        up=[]
        down=[]
        while len(up)<4:
            new_pair = letter_choice()
            if new_pair[0] not in up and new_pair[1] not in down:
                up.append(new_pair[0])
                down.append(new_pair[1])

        if random.choice([True, False]):
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


def word_meaning():
    csv_to_dict = []
    with open ('pairs.csv', 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)
        for col in data:
            csv_to_dict.append({'pair1':col['pair1'],'pair2':col['pair2'],'word_type':col['type']})
    random_pair = random.choice(csv_to_dict)
    word1 = random_pair['pair1']
    word2 = random_pair['pair2']
    pair_type = random_pair['word_type']
    word3_choices = [[x['pair1'],x['pair2']] for x in csv_to_dict if x['word_type'] == pair_type and x['pair1'] != word1]
    word3 = random.choice(random.choice(word3_choices))
    question = [word1,word2,word3]
    random.shuffle(question)
    return question, word3


def reasoning():

    def make_fact(word_type:int, word: str) -> str:
        str_fact = ''
        if word_type == 1:
            str_fact = f' is not as {word} as '
        elif word_type ==2:
            str_fact = f' is {word} than '
        elif word_type == 3 or word_type == 4:
            str_fact = f' has {word} than '
        elif word_type == 5:
            str_fact= f' is {word} than '
        return str_fact

    def make_question(word_type:int, word: str) -> str:
        str_question = ''
        if word_type ==2:
            str_question = f'Who is {word}?'
        elif word_type == 3 or word_type == 4:
            str_question = f'Who has {word}?'
        elif word_type == 5:
            str_question= f'Who is {word}?'
        return str_question

    names = ['John','Ben','Vince','Brad','Matt', 'Anna','Lea','Alice','Julie']
    csv_to_dict = []
    with open ('reasoning.csv', 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)
        for col in data:
            if col['type']=='1':
                answerA = col['opposite']
                answerB = col['same']
            else:
                answerA= col['same']
                answerB=col['opposite']
            csv_to_dict.append({'id': col['id'], 'word': col['word'], 'type': col['type'],
                                'same': col['same'], 'opposite': col['opposite'], 'answerA': answerA,
                                'answerB': answerB})
    names = dict(zip(['answerA','answerB'], random.sample(names,2)))
    row_fact = random.choice(csv_to_dict)
    fact = f'{names["answerA"]}{make_fact(int(row_fact["type"]),row_fact["word"])}{names["answerB"]}'
    answer = random.choice(['answerA','answerB'])
    id_question = random.choice(row_fact[answer].split(','))
    print(fact)
    print(id_question)
    row_question = [x for x in csv_to_dict if x['id'] == id_question]
    print(row_question)
    if not row_question:
        print(f"Answer {answer}")
        print(f"Row fact {row_fact}")
        print(f"No question found for id {id_question}")
    else:
        question = make_question(int(row_question[0]['type']), row_question[0]['word'])    
    name_answer = names[answer]
    return [fact, question, list(names.values())], name_answer

