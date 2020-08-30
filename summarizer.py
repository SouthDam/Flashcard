from transformers import (
    BartTokenizer, 
    BartForConditionalGeneration, 
    BartConfig,
    AutoModelWithLMHead, 
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)
from preprocess import get_intro, get_full
import torch
from time import time
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures

executor= ProcessPoolExecutor()
# executor can't be put in the class, otherwise 
# it would produce weakref object which could not be pickled

class Summarizer():
    def __init__(self):
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.model.to(self.device)

    def ForRough(self, name):
        """
        The input should be the name of a wikipedia page
        The output is the summary of its introduction part
        """
        time_start=time()
        text = get_intro(name)
        print("Text read")
        time_end=time()
        print('read time cost',time_end-time_start,'s')
        # summary of paragraphs
        time_start=time()
        para_summary = self.summarize(text)
        para_summary = [para_summary]
        # final output summary
        summary = self.summarize(para_summary,stage=2)
        time_end=time()
        print('summary time cost',time_end-time_start,'s')
        return summary

    def ForIntro(self, name):
        """
        The input should be the name of a wikipedia page
        The output is the paragraph summaries of its introduction part
        """
        time_start=time()
        text = get_intro(name)
        print("Text read")
        time_end=time()
        print('read time cost',time_end-time_start,'s')
        time_start=time()
        summary = self.summarize(text)
        time_end=time()
        print('summary time cost',time_end-time_start,'s')
        return summary

    def ForFullRough(self, name):
        """
        The input should be the name of a wikipedia page
        The output is the section-wise summaries of its content
        """
        time_start=time()
        text_dict = get_full(name)
        print("Text read")
        time_end=time()
        print('read time cost',time_end-time_start,'s')
        ss = {}
        time_start=time()
        for key, value in text_dict.items():
            # if section has no subsections
            if type(value)==list:
                pre_summary = self.summarize(value)
                summary = self.summarize([pre_summary],stage=2)
                ss[key] = summary
            # if section has subsections
            elif type(value)==dict:
                this_value={}
                for subkey, subvalue in value.items():
                    pre_summary = self.summarize(subvalue)
                    summary = self.summarize([pre_summary],stage=2)
                    this_value[subkey] = summary
                ss[key] = this_value
        time_end=time()
        print('summary time cost',time_end-time_start,'s')
        return ss

    def ForFull(self, name):
        """
        The input should be the name of a wikipedia page
        The output is the paragraph-wise summaries of its content
        """
        time_start=time()
        text_dict = get_full(name)
        print("Text read")
        time_end=time()
        print('read time cost',time_end-time_start,'s')
        ss = {}
        time_start=time()
        for key, value in text_dict.items():
            # if section has no subsections
            if type(value)==list:
                summary = self.summarize(value)
                ss[key] = summary
            # if section has subsections
            elif type(value)==dict:
                this_value={}
                for subkey, subvalue in value.items():
                    summary = self.summarize(subvalue)
                    this_value[subkey] = summary
                ss[key] = this_value
        time_end=time()
        print('summary time cost',time_end-time_start,'s')
        return ss
    
    def summarize(self,p,stage=1):
        if self.device=="cpu":
            return self.parallel_summarize(p,stage)
        elif self.device=="cuda":
            return self.cuda_summarize(p,stage)
        else:
            pass

    def cuda_summarize(self, p, stage=1):
        """
        Input: a list of string, ideally list of paragraphs
        Output: string, combination of summaries of input strings
        """
        summary = str()
    
        for i in range(len(p)):
            if len(p[i])<50:
                continue
            if stage==1:
                ip = self.tokenizer.encode("summarize: "+p[i], return_tensors="pt", max_length=1024, truncation=True)
                op = self.model.generate(ip, max_length=250, length_penalty=2.0, num_beams=4, early_stopping=True)
            if stage==2:
                ip = self.tokenizer.encode("summarize: "+p[i], return_tensors="pt", max_length=1024, truncation=True)
                op = self.model.generate(ip, max_length=250, min_length=80, length_penalty=2.0, num_beams=4, early_stopping=True)
            op = self.tokenizer.decode(op[0],skip_special_tokens=True)
            if op[-1] != ".":
                op += "."
            summary += op
            summary += " "
        summary=summary[:-1]
        return summary
    
    def generate1(self,ip):
        return self.model.generate(ip, max_length=150, min_length=0, length_penalty=2.0, num_beams=4, early_stopping=True)
    
    def generate2(self,ip):
        return self.model.generate(ip, max_length=150, min_length=80, length_penalty=2.0, num_beams=4, early_stopping=True)

    def parallel_summarize(self,p,stage=1):
        """
        Input: a list of string, ideally list of paragraphs
        Output: string, combination of summaries of input strings
        """
        summary = str()
        ip=[]
        for i in range(len(p)):
            if len(p[i])<50:
                continue
            ip.append(self.tokenizer.encode("summarize: "+p[i], return_tensors="pt", max_length=1024, truncation=True))
        if stage==1:
            ge = executor.map(self.generate1,ip)
        if stage==2:
            ge = executor.map(self.generate2,ip)
        for op in ge:
            op = self.tokenizer.decode(op[0],skip_special_tokens=True)
            if op[-1] != ".":
                op += "."
            summary += op
            summary += " "
        summary=summary[:-1]
        return summary
