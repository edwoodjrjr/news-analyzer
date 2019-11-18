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

    insult_str = j['insult']
    remove_table = dict.fromkeys(map(ord, '+"@#$'), None)
    insult_str = insult_str.translate(remove_table)
    insult_str_len = len(insult_str)

    print('Insult: ' + insult_str)
    units = str(math.ceil((insult_str_len/1000)*2))
    print('Number of Google Natural Language units used processing this insult: ' + units)

    doc_data = analyze_sentiment(insult_str)
    entity_data = []
    entity_response = analyze_entity_sentiment(insult_str)
    for entity in entity_response.entities:
        sentiment = entity.sentiment
        entity_data.append({'entity_name': entity.name, 'entity_score': sentiment.score, 'entity_magnitude': sentiment.magnitude, 'entity_salience': entity.salience})

    html = render_template('insult.html', text=insult_str, score=doc_data.document_sentiment.score, magnitude=doc_data.document_sentiment.magnitude, entities=entity_data, usage=units)
    
    return html

@app.route("/news")
def news():
    subject = request.args.get('subject', default = '', type = str)
    news_api_key = os.environ['NEWSAPIKEY']
    url = ('https://newsapi.org/v2/top-headlines?'
       'q=' + subject + '&'
       'country=us&'
       'language=en&'
       'apiKey=' + news_api_key)
    r = requests.get(url)
    j = r.json()
    news_str = ''

    for k,v in j.items():
        if k == "articles":
            articles_json = v
            for article in articles_json:
                description = str(article['description'])
                news_str = news_str + description + ' '
    
    remove_table = dict.fromkeys(map(ord, '+"@#$'), None)
    news_str = news_str.translate(remove_table)
    news_str_len = len(news_str)

    print('News: ' + news_str)
    units = str(math.ceil((news_str_len/1000)*2))
    print('Number of Google Natural Language units used processing this news: ' + units)

    doc_data = analyze_sentiment(news_str)
    entity_data = []
    entity_response = analyze_entity_sentiment(news_str)
    for entity in entity_response.entities:
        sentiment = entity.sentiment
        entity_data.append({'entity_name': entity.name, 'entity_score': sentiment.score, 'entity_magnitude': sentiment.magnitude, 'entity_salience': entity.salience})

    if subject == '':
        subject = 'everything'

    html = render_template('news.html', subject=subject, score=doc_data.document_sentiment.score, magnitude=doc_data.document_sentiment.magnitude, entities=entity_data, usage=units)
    
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

    return response

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
 
    return response