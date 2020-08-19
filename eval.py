import numpy as np
from sentence_transformers import SentenceTransformer 

class cos():
    def __init__(self):
        self.sm = SentenceTransformer('bert-large-nli-stsb-mean-tokens')
    
    def eval(self,original,summary):
        """
        Evaluate the similarity between original text and summary text
        """
        if type(original)==str:
            original=self.get_st(original)
        if type(summary)==str:
            summary=self.get_st(summary)
        ori_embeddings = self.sm.encode(original)
        sum_embeddings = self.sm.encode(summary)
        ori_vec = self.new_vector(ori_embeddings)
        sum_vec = self.new_vector(sum_embeddings)
        return self.cosine(ori_vec,sum_vec)
        
    def new_vector(self,vectors):
        """
        Add up sentence embeddings of a paragraph to get a paragraph vector
        """
        for i,v in enumerate(vectors):
            vectors[i]=np.array(v)
        vector = np.zeros(1024)
        for __, v in enumerate(vectors):
            vector += v
        return vector

    def get_st(self,text):
        """
        turn string into list for later computation
        """
        text = text.split('.')
        for i, sentence in enumerate(text):
            text[i] = sentence + "."
        if text[-1]==".":
            text = text[:-1]
        return text

    def cosine(self,a,b):
        """
        compute cosine similarity of two vectors
        """
        a=np.array(a)
        b=np.array(b)
        up=np.dot(a,b)
        down_sq=np.dot(a,a)*np.dot(b,b)
        down=np.sqrt(down_sq)
        return up/down