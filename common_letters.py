import random

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

def question():
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
    return up,down

def get_nb_of_pairs(up, down):
    score = 0
    for u,d in zip(up,down):
        if u.lower() == d.lower():
            score += 1
    return score





