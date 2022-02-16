from dataclasses import dataclass
from typing import List,Dict
import random

# Not used for now
@dataclass
class Adjectives:
    name:str
    comparative: str
    synonymes: List['Adjectives']
    antonymes: List['Adjectives']
    linked_nouns: List[str]



names = ['John','Ben','Vince','Brad','Matt']
adjectives = {'tall':{'comparative':'taller','antonyms':['small']},
              'small':{'comparative':'smaller','antonyms':['tall']}
              }

def generate_situation():
    name1,name2 = random.sample(names, 2)
    chosen_adjective = random.choice(list(adjectives.keys()))
    positive = random.getrandbits(1)
    return name1,name2,chosen_adjective,positive

def phrase_situation(name1,name2,adjective,positive):
    if positive == 0:
        situation = f'{name1} is not as {adjective} as {name2}'
    else:
        adjective = adjectives[adjective]['comparative']
        situation = f'{name1} is {adjective} than {name2}'
    return situation

def extract_adjective_for_question(adjective:str):
    possibilities = [adjective]
    antonyms = adjectives[adjective]['antonyms']
    for antonym in antonyms:
        possibilities.append(antonym)
    return random.choice(possibilities)

def phrase_question(adjective_for_question:str):
    return f'Who is {adjectives[adjective_for_question]["comparative"]}?'

def get_answer(name1,name2,adj_s,positive:bool,adj_q):
    if adj_s == adj_q and positive:
        return name1
    elif adj_s == adj_q and not positive:
        return name2
    elif adj_s != adj_q and positive:
        return name2
    elif adj_s != adj_q and not positive:
        return name1





# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
