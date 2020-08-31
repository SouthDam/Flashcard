from summarizer import Summarizer
from QG import QueGenerator
import wikipedia
import pandas as pd

names = wikipedia.random(1000)
print("names generated")
bart = Summarizer()
qg = QueGenerator()
our_length =pd.DataFrame(columns=('input_length','summary_length','question_generated_num','question_kept_num'))
for idx, name in enumerate(names):
    try:
        input_raw_text = wikipedia.summary(name)
        input_length = len(input_raw_text.split())
        summary = bart.ForIntro(name)
        summary_length = len(summary.split())
        cards = qg.generate(summary,name)
        questions_generated_num = len(cards)
        questions_kept = [card for card in cards if card["isGood"]]
        questions_kept_num = len(questions_kept)
        our_length.loc[idx] = {'input_length':input_length,'summary_length':summary_length,'question_generated_num':questions_generated_num,'question_kept_num':questions_kept_num}
    except:
        pass
    if idx%10==0:
        file_name="anaysis-"+str(int(idx/10)+1)+".csv"
        our_length.to_csv(file_name,index=False)
        print("finish batch"+str(int(idx/10)+1))
        our_length =pd.DataFrame(columns=('input_length','summary_length','question_generated_num','question_kept_num'))
