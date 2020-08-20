from QG import QueGenerator

qg = QueGenerator()

def omit(summary):
    """
    INPUT: string
    OUTPUT: print flashcards on the screen
    """
    cards = qg.generate(summary)
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