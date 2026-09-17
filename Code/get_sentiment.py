#!/opt/homebrew/bin/python3.12
# Get the sentiment of a sentence

import os
from transformers import pipeline
import torch

import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def Get_Sentiment(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)

    neg=scores['neg']
    pos=scores['pos']
    if pos > neg:
        classifier='positive'
    elif neg > pos:
        classifier='negative'
    else:
        classifier='neutral'
    return classifier