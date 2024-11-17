# V4Fire chatbot
Documentation chatbot for V4Fire framework based on RAG


## How to run?

1. Install requirements
```
pip install -r requirements.txt
```

2. Setup packages
```
pip install -e .
```

3. Create .env and define the following variables 

> GITHUB_TOKEN \
> GOOGLE_API_KEY \
> BOT_TOKEN

4. Populate database (later i will push it to repo)

Run src/db_prep/pipeline.py

5. Start bot

Run src/frontend/main.py
