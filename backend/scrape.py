import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json

# Neutral
# url="https://timesofindia.indiatimes.com/city/varanasi/pm-modi-to-be-main-yajman-at-ram-temple-event/articleshow/106907765.cms"

# Positive
# url="https://timesofindia.indiatimes.com/life-style/soul-search/the-true-meaning-of-love-and-romance-explained-by-sadhguru/articleshow/106971631.cms"

# Negitive
# url="https://timesofindia.indiatimes.com/city/ludhiana/4-killed-2-injured-in-car-truck-collision-on-jammu-jalandhar-national-highway/articleshow/107178539.cms"
response= requests.get(url)

if response.status_code==200:
    soup=BeautifulSoup(response.text, "html.parser")


    # To get the heading data
    heading=soup.find(class_="HNMDR")
    # print(data.get_text)
    # Check if the element is found before calling get_text
    if heading:
        content_inside_span = heading.find('span').get_text(strip=True)
        print("@ 0 content_inside_span", content_inside_span)
        modified_content_inside_span = content_inside_span.replace('\u2018', '').replace('\u2019', '')
        # again_modified_content_inside_span = content_inside_span.replace('\u2019', '')
        # updated_text = re.sub(r'\s+', ' ', heading)
        # # updated_text = cleaned_text.replace(text_to_reject, '')
        # print(updated_text)
    else:
        print("@ 4 Element with class 'HNMDR' not found on the page.")



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

    with open("input_for_model.json", "w") as json_file:
        json_data=json.dump(scrapped_Data_Dictonary, json_file, indent=4)

    print("@5 Data saved to input_for_model.json successfully.")
else:
    print(f"@ 6Failed to retrieve the page. Status code: {response.status_code}")