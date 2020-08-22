from QG import QueGenerator
from time import time

qg = QueGenerator()

def omit(summary,title):
    """
    INPUT: string
    OUTPUT: print flashcards on the screen
    """
    time_start=time()
    cards = qg.generate(summary,title)
    time_end=time()
    print('generate time cost',time_end-time_start,'s')
    print("     ")
    print("     ")
    print(summary)
    print("     ")
    print("Questions for you: ")
    # output questions and answers which are good enough
    for card in cards:
        if card["isGood"]:
            print(card["question"])
    print("Hints: ")
    for card in cards:
        if card["isGood"]:
            print(card["answer"])