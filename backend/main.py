from bs4 import BeautifulSoup
import re

from fastapi import FastAPI, Query,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from typing import List, Dict, Any

import requests
import json


import os
from os.path import exists


import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",


]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the TF-IDF vectorizer
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Load the trained logistic regression model
loaded_model = joblib.load('model.pkl')

class AnalyzeRequest(BaseModel):
    tweetLink: str

class AnalyzeResponse(BaseModel):
    result: str

@app.get("/")
def root():
    return{"status":"Up and running."}


@app.get("/analyse")
async def analyze(newsLink: str = Query(..., description="Link to the tweet")):
    try:
        headline = await scrapeTweetText(newsLink)
        analyzed_result = await sentiment_classifier(headline)
        return{"result":analyzed_result}
        
    except Exception as e:
        return {"result": str(e)}



async def scrapeTweetText(url):
    response= requests.get(url)

    if response.status_code==200:
        soup=BeautifulSoup(response.text, "html.parser")


        # To get the heading data
        heading=soup.find(class_="HNMDR")
        # print(data.get_text)
        if heading:
            content_inside_span = heading.find('span').get_text(strip=True)
            print("@6 content_inside_span", content_inside_span)
            modified_content_inside_span = content_inside_span.replace('\u2018', '').replace('\u2019', '')
        
        else:
            print("@5 Element with class 'HNMDR' not found on the page.")


        # scrapped_Data_Dictonary={}
        input=modified_content_inside_span
        scrapped_Data_Dictonary={
            "category": "News",
            "headline": input,
            "authors": "TOI",
            "link": url,
            "short_description": "ChatGPT",
            "date": "TS"
        }
        return scrapped_Data_Dictonary["headline"]
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return "Something went wrong."




async def sentiment_classifier(headline):
    print("@1 Headline", headline)
      # Replace with the actual file name


    try:
        loaded_model = joblib.load('model.pkl')  # Replace with the actual file name
            # Load the TF-IDF vectorizer used during training
        tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

        my_series = pd.Series([headline])
        print("@2 news_x", my_series)
        new_X = tfidf_vectorizer.transform(my_series) 
        # Transform the new data using the loaded TF-IDF vectorizer
        print("@2 news_x", new_X)

   
        new_predictions = loaded_model.predict(new_X)  # Use the loaded model to make predictions
        print("@--7 news_predictions", new_predictions)
        return new_predictions[0]

    
    except Exception as e:
        return {"result": str(e)}

    