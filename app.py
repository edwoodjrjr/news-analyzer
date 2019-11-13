#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------

# add web form to take input for news source, subject

import os
import json
import requests
import math

from flask import Flask
app = Flask(__name__)

from google.cloud import language_v1
from google.cloud.language_v1 import enums

@app.route("/insult")
def insult():
    #return app.send_static_file("index.html")
    url = 'https://evilinsult.com/generate_insult.php?lang=en&type=json'
    r = requests.get(url)
    j = r.json()
    return sample_analyze_sentiment(j["insult"])

@app.route("/news")
def news():
    newsapikey = os.environ['NEWSAPIKEY']
    url = ('https://newsapi.org/v2/top-headlines?'
       #'q=Trump&'
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
    print('Number of Google Natural Language units used: ' + str(math.ceil(new_str_len/800)))
    return new_str
    #return sample_analyze_sentiment(new_str)

def sample_analyze_sentiment(text_content):
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

    print(u"Response text: {}".format(text_content))
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(u"Document sentiment magnitude: {}".format(response.document_sentiment.magnitude))

    # for sentence in response.sentences:
    #     print(u"Sentence text: {}".format(sentence.text.content))
    #     print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
    #     print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    print(u"Language of the text: {}".format(response.language))

    response_json = {"text": text_content, "sentiment_score": response.document_sentiment.score, "sentiment_magnitude": response.document_sentiment.magnitude, "language": language}

    return json.dumps(response_json, sort_keys=False)