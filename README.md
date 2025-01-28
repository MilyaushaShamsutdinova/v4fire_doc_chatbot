# V4Fire chatbot
Documentation chatbot for V4Fire framework based on RAG. Project utilizes *Retrieval-Augmented Generation* (**RAG**) and *Recursive Abstractive Processing for Tree-Organized Retrieval* (**RAPTOR**) techniques to provide automated, AI-based answers about the V4Fire framework. The chatbot integrates with third-party LLM such as Gemini AI and it is served in Telegram bot. Key feature is ability to answer to questions of different complexity.

## App architecture

The app is served using a Telegram bot. In the backend, RAG system is implemented with an additional database to store question-answer pairs, reducing unnecessary usage of the LLM.

![app architecture](https://github.com/MilyaushaShamsutdinova/v4fire_doc_chatbot/blob/main/assets/App_architecture_.png?raw=true)

For the LLM, I used the Gemini AI API, specifically the Gemini 1.5 Flash version. 

## DB creation pipeline

Before launching the system, it is necessary to create and populate the database with chunks of V4Fire documentation. Here, the RAPTOR approach is implemented.

First, I fetched data from the [V4Fire Core](https://github.com/V4Fire/Core) and [V4Fire Client](https://github.com/V4Fire/Client) repositories containing the documentation. These original documents were stored in the database, naturally chunked according to the framework’s components.

![db population pipeline](https://github.com/MilyaushaShamsutdinova/v4fire_doc_chatbot/blob/main/assets/DB_creation_pipeline_.png?raw=true)

The RAPTOR approach involves storing documents in a tree-like structure, where each node contains summaries of the documents from the previous level, while the original documents are stored in the leaf nodes.

In the diagram, the cycle of clustering and summary generation indicates the ability to perform multiple levels of summarization. I decided to create 2 levels of summarization.

## Retrieval system

The retrieval system is enhanced by the RAPTOR approach. When a query is passed into the system, its complexity is estimated using a simple rule-based function based on query keywords. 

![retrieval](https://github.com/MilyaushaShamsutdinova/v4fire_doc_chatbot/blob/main/assets/Retrieval_system_.png?raw=true)

Each query is assigned a complexity level:

- 0 - Complex query
- 1 - Medium complexity
- 2 - Simple, surface-level query

For each query, relevant documents are extracted from the corresponding summary level of the RAPTOR tree database. After retrieving the top 5 similar documents, an additional filtering step is applied to ensure only highly relevant documents are selected based on a threshold.


## Pros & Cons

| Advantages  | Disadvantages |
| ------------- | ------------- |
| Ability to answer general questions  | No context capturing along in the chatbot  |
| Faster response for question already answered  | Bot cannot write fully working code  |
|    | Not convenient interface for coding tool, it would be more appropriate to create VS code extension, probably  |

All the disadvantages are actually a space for further improvements :)

## How to run?

1. Create .env and define the following variables 

> GITHUB_TOKEN \
> GOOGLE_API_KEY \
> BOT_TOKEN

2. Turn on VPN if you're in Russia \
It is needed for using Gemini API.


3. Build the image of container
```
docker-compose build
```

4. Start bot 

```
docker-compose up
```
