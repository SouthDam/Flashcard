from summarizer import Summarizer
from QG import QueGenerator
import wikipedia
import pandas as pd

names=["Italy","China"]
bart = Summarizer()
qg = QueGenerator()
our_length =pd.DataFrame(columns=('input_length','summary_length','question_generated_num','question_kept_num'))
for name in names:
    try:
        input_raw_text = wikipedia.summary(name)
        input_length = len(input_raw_text.split())
        print(input_length)
        summary = bart.ForIntro(name)
        summary_length = len(summary.split())
        print(summary_length)
        cards = qg.generate(summary,name)
        questions_generated_num = len(cards)
        print(questions_generated_num)
        questions_kept = [card for card in cards if card["isGood"]]
        questions_kept_num = len(questions_kept)
        print(questions_kept_num)
        our_length=our_length.append(pd.DataFrame({"input_length":[input_length],"summary_length":[summary_length],"question_generated_num":[questions_generated_num],"question_kept_num":[questions_kept_num]}),ignore_index=True)
    except:
        pass
print(our_length)