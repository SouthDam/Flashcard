# from wiki name to flashcards
from summarizer import Summarizer
from generator import omit
import wikipedia

if __name__=="__main__":
    print("Please ignore the following warnings.")
    # initiate summarizer
    bart = Summarizer()
    # initiate question generator
    # qg = QueGenerator(model_dir="/Users/southdam/Desktop/Master-Project-Flashcard")
    # force the code to run repeatly to save the time from
    # loading models if users would like to generate flashcards multiple times
    while True: 
        while True:
            name = input("Please input a name of a wikipedia page (input break to terminate): ")
            if name=="break":
                break
            try:
                wikipedia.summary(name)
                break
            except:
                print("Your input name may refer to more than one page. (ambiguous)")
        if name=="break":
            break
        while True:
            level = input("Please input the level you want [highlight/intro/rough/full]: ")
            if level == "highlight" or level == "intro" or level == "rough" or level == "full":
                break
            else:
                print("Looks like you typed something wrong :)")
    
        # generate summary
        for __ in range(10):
            print("    ")
        print("Process Started")
        if level == "highlight":
            summary = bart.ForRough(name)
        elif level == "intro":
            summary = bart.ForIntro(name)
        elif level == "rough":
            summary = bart.ForFullRough(name)
        elif level == "full":
            summary = bart.ForFull(name)
        else:
            pass
        print("Finished summarization")
        if type(summary)==str:
            omit(summary)
        elif type(summary)==dict:
            for key, value in summary.items():
                if type(value)==str:
                    print(key)
                    omit(value)
                elif type(value)==dict:
                    print(key)
                    for subkey, subvalue in value.items():
                        print(subkey)
                        omit(subvalue)
                else:
                    pass