# News Sentiment Analyzer

This is a project based on **[VS Code Remote - Containers](https://aka.ms/vscode-remote/containers)** 

This will grab the top headlines from a news API and run them through the Google Natural Language API sentiment analyzer.

Requirements: 
- VSCode with the Remote Containers extension
- environment.env and gcloudkey.json files in the root folder.
    - environment.env contents:
        - GOOGLE_APPLICATION_CREDENTIALS=gcloudkey.json
        - NEWSAPIKEY='apiKey from newsapi.org'
    - gcloudkey.json contents: A private key in JSON format for a Google cloud service account that has access to a project where the Google Natural Language API is enabled