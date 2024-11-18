# V4Fire chatbot
Documentation chatbot for V4Fire framework based on RAG. Project utilizes RAG and RAPTOR techniques to provide automated, AI-based answers about the V4Fire framework. The chatbot integrates with third-party LLM such as Gemini AI and it is served in Telegram bot. Key features include efficient document parsing and ability to answer to questions of different complexity. 


## How to run?

1. Create .env and define the following variables 

> GITHUB_TOKEN \
> GOOGLE_API_KEY \
> BOT_TOKEN

2. Turn on VPN if you're in Russia


3. Build the image of container
```
docker-compose build
```

4. Start bot 

```
docker-compose up
```
