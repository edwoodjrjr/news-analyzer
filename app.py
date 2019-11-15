#-----------------------------------------------------------------------------------------
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------

# add timer to prevent too many requests
# add CSS

import os
import json
import requests
import math

from flask import Flask, render_template, request
app = Flask(__name__)

from google.cloud import language_v1
from google.cloud.language_v1 import enums

@app.route("/insult")
def insult():
    url = 'https://evilinsult.com/generate_insult.php?lang=en&type=json'
    r = requests.get(url)
    j = r.json()
    
    sentiment_str = analyze_insult(j["insult"])
    sentiment_json = json.loads(sentiment_str)

    burn = sentiment_json["text"]
    score = sentiment_json["sentiment_score"]
    magnitude = sentiment_json["sentiment_magnitude"]

    return render_template('insult.html', text=burn, score=score, magnitude=magnitude)

@app.route("/news")
def news():
    subject = request.args.get('subject', default = '', type = str)
    newsapikey = os.environ['NEWSAPIKEY']
    url = ('https://newsapi.org/v2/top-headlines?'
       'q=' + subject + '&'
       'country=us&'
       'language=en&'
       'apiKey=' + newsapikey)
    r = requests.get(url)
    j = r.json()
    new_str = ''

    for k,v in j.items():
        if k == "articles":
            articles_json = v
            for article in articles_json:
                description = str(article['description'])
                new_str = new_str + description + ' '
    
    remove_table = dict.fromkeys(map(ord, '+"@#$'), None)
    new_str = new_str.translate(remove_table)
    new_str_len = len(new_str)

    print('News: ' + new_str)
    print('Number of Google Natural Language units used: ' + str(math.ceil((new_str_len/1000)*2)))

    document_sentiment_data = analyze_sentiment(new_str)
    entity_sentiment_data = analyze_entity_sentiment(new_str)

    if subject == '':
        subject = 'everything'

    html = render_template('news.html', subject=subject, score=document_sentiment_data[0]['sentiment'], magnitude=document_sentiment_data[0]['magnitude'], entities=entity_sentiment_data)
    
    return html

def analyze_insult(text_content):
    """
    Analyzing Sentiment in a String
    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_sentiment(document, encoding_type=encoding_type)

    response_json = {"type": "sentiment analysis", "text": text_content, "sentiment_score": response.document_sentiment.score, "sentiment_magnitude": response.document_sentiment.magnitude, "language": language}
    return json.dumps(response_json, sort_keys=False)

def analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze

    """

    client = language_v1.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_sentiment(document, encoding_type=encoding_type)

    data = [{'sentiment': response.document_sentiment.score,'magnitude': response.document_sentiment.magnitude, 'language': response.language}]

    return data

def analyze_entity_sentiment(text_content):
    """
    Analyzing Entity Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
    data = []

    for entity in response.entities:
        sentiment = entity.sentiment
        data.append({'entity_name': entity.name, 'entity_score': sentiment.score, 'entity_magnitude': sentiment.magnitude, 'entity_salience': entity.salience})
 
    return data