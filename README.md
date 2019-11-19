# News Sentiment Analyzer

This is a project based on **[VS Code Remote - Containers](https://aka.ms/vscode-remote/containers)** 

This will grab the top headlines from a news API and run them through the Google Natural Language API sentiment analyzer.  You can use this information to decide if you want to get up in the morning, or stay in bed.

Requirements: 
- Microsoft Visual Studio Code with the Remote Containers extension installed.
- environment.env and gcloudkey.json files in the root folder.
    - environment.env contents:
        - GOOGLE_APPLICATION_CREDENTIALS=gcloudkey.json 
        - NEWSAPIKEY='apiKey from newsapi.org' (see https://newsapi.org/docs/get-started for info on how to get an API key)
    - gcloudkey.json contents: A private key in JSON format for a Google cloud service account that has access to a project where the Google Natural Language API is enabled (see https://cloud.google.com/natural-language/docs/quickstart-client-libraries for info on setting up a project and service account)

Example command to run the server from a Python virtualenv (aka without VSCode's help):
- export FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=0 GOOGLE_APPLICATION_CREDENTIALS=gcloudkey.json NEWSAPIKEY=<your newsapi.org API key>
- flask run --host 0.0.0.0 --port 9000 &