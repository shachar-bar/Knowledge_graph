#!/opt/homebrew/bin/python3.12
# This is the main function of the RQ research project runtime

import os
import sys
import re

import time
import nltk
from nltk.translate.bleu_score import sentence_bleu

import spacy

from get_sentiment import Get_Sentiment
from pos import Convert_to_dict_tuple

def KB_Converter(text):
    # Convert text with Conference Resolutions and split it into sentences.
    return text

def sentence_converter(sentence,Prompt_Nodes,SoT,Color,Prompt):
    
    Nodes,Edges,Correlated_Nodes=pos_parser(sentence,Prompt_Nodes)
    
    New_Edges,[]=Convert_to_dict_tuple(SoT,Nodes,Edges,Color,Prompt)

    for node in Nodes:
        if node not in Total_nodes:
            Total_nodes.append(node)
    for edge in New_Edges:
        From_node=edge[0]
        To_node=edge[1]
        if From_node == To_node:
            continue
        for p_node in Prompt_Nodes:
            if p_node in From_node or p_node.lower() in From_node:
                New_Edge_reg=(p_node,From_node,{'weight':1,'val':'-','color':'blue'},SoT)
                New_Edge_lower=(p_node.lower(),From_node,{'weight':1,'val':'-','color':'blue'},SoT)
                if New_Edge_reg not in New_Edges and New_Edge_lower not in New_Edges:
                    New_Edges.append(New_Edge_reg)
            if p_node in To_node or p_node.lower() in To_node:
                New_Edge_reg=(p_node,To_node,{'weight':1,'val':'-','color':'blue'},SoT)
                New_Edge_lower=(p_node.lower(),To_node,{'weight':1,'val':'-','color':'blue'},SoT)
                if New_Edge_reg not in New_Edges and New_Edge_lower not in New_Edges:
                    New_Edges.append(New_Edge_reg)
        Total_edges.append(edge)
    return Total_nodes,Total_edges

def Read_KB(KB_File):
    try: 
        FILE=open(KB_File,'r')
    except FileNotFoundError:
        print (f"The path {KB_File} cannot be found")
        sys.exit(1)

    Contents_str=(FILE.readline()).strip() 
    FILE.close()
    try:
        Contents=(Contents_str.split(':',1))[1]
    except:
        Contents=''
    
    Array_Contents=Contents.split("', '")
    Sentences_List=[]
    for elem in Array_Contents:
        count = len(re.findall(r"\w\. ", elem))
        if count > 0:
            elem_list=re.split(r"\. ", elem)
            for new_elem in elem_list:
                Sentences_List.append(new_elem)
        else:
            Sentences_List.append(elem)
  
    KB_Contents=[]

    for sentence in Sentences_List:
        if len(sentence) < 10:
            continue

        try:
            if sentence[0] == '[' or sentence[0] == ']' or sentence[0] == "'":
                sentence=sentence[1:]
        except:
            pass
        sentence_len=len(sentence)

        KB_Contents.append(sentence)
    return SoT,Author,Published,KB_Contents

if __name__ == "__main__":

    start_time = time.perf_counter()
  
    try:
        Prompt = os.environ.get("Prompt")
        KB_Path = os.environ.get("KB_Path")
    except:
        print("Please set both Prompt and KB_Path environment variables.")
        sys.exit(0)

    if Prompt == "" or Prompt == None:
        print (f"Please set the Prompt env. variable or comment this line and uncomment one of the below variable settings.")
        sys.exit(1)

    Top_High_Quality_Sentences=100

    if KB_Path == "" or KB_Path == None:
        print (f"Please set the KB_Path env. variable or comment this line and uncomment one of the below variable settings.")
        sys.exit(2)

    try:
        KB_Path
    except:
        print ("The knwoledge base path variable - KB_Path is not defined!")
        sys.exit(1)

    try:
        KB_Entries=os.listdir(KB_Path)
        print (f"KB_Entries: {KB_Entries}")
    except:
        print (f"Can't read the directory {KB_Path}!")
        sys.exit(1)
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    All_Nodes=[]
    All_Edges=[]
    SoTs=[]
    Full_SoTs=[]

    Prompt_Nodes=[]
    Prompt_Edges=[]
    Prompt_Nodes,Prompt_Edges,[]=pos_parser(Prompt, Prompt_Nodes)
    Prompt_Sentiment=Get_Sentiment(Prompt)
    
    nlp_eval = spacy.load("en_core_web_lg")
    Evaluation=[]

    for KB_File in KB_Entries:
        SoT_File=KB_Path+'/'+KB_File
        SoT,Author,Published,Knowledge_base=Read_KB(SoT_File)
        Full_SoT=f"{SoT}\n{Author}\n{Published})"
        SoTs.append(SoT)
        Full_SoTs.append(Full_SoT)

        if len(Knowledge_base) == 0:
            continue

        Clean_KB = [element.replace("\\", "") for element in Knowledge_base]

        Pronouns=['he','she','they','it','him','his','her','hers','them','their','theirs']
        word_list = (" ".join(Clean_KB)).split()
        Flag=0
        for word in word_list:
            if word.lower() in Pronouns:
                Flag=1
        if Flag == 1:
            Reduced_KB=KB_Converter(Clean_KB)
        else:
            Reduced_KB=Clean_KB
        
        for text in Reduced_KB:
            Sentiment=Get_Sentiment(text)
            
            if Sentiment == 'positive':
                Color='green'
            elif Sentiment == 'negative':
                Color='red'
            else:
                Color='blue'
            Edges,Constructed_sentence=Convert_to_dict_tuple(SoT,Nodes,Edges,Color,Prompt)
                      
            Sim=Get_Similarity_Score(nlp_eval,text,Constructed_sentence)

            original_tokens=text.split()
            constructed_tokens=Constructed_sentence.split()
            Bleu_ref_list=[original_tokens]
            Bleu_score=sentence_bleu(Bleu_ref_list,constructed_tokens)
            
            Evaluate={'original':text,'constructed':Constructed_sentence,'similarity':Sim,'Bleu':Bleu_score,'SoT':SoT}
            Evaluation.append(Evaluate)
    
            for Correlated_Node in Correlated_Prompt_Nodes: 
    
                if Correlated_Node not in Nodes: 
                    Nodes.append(Correlated_Node)
                for node in Nodes:
                    if DEBUG: 
                        if node=='':
                            continue
                    try:
                        Edges.append(Correlated_Node,node,{'weight':{1},'val':{'-'},'color':{Color}},SoT) 
                    except:
                        pass
            for node in Nodes:
                All_Nodes.append(node)

            for edge in Edges:
                All_Edges.append(edge)

    with open(DST, 'w', encoding='utf-8') as file:
        file.write(f"Execution time: {end_time - start_time:.2f} seconds")
    file.close()