import google.generativeai as genai
from google.api_core import retry
from dotenv import load_dotenv
import os
import time


class GeminiAI:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
    def get_response(self, request: str, content: str):
        """
        Generates a response for a given user request using relevant documentation content.

        This method constructs a prompt containing the user request and relevant documentation
        data, and sends it to the generative model to generate a response. The response is
        formatted specifically for Telegram, adhering to guidelines such as bolding important
        concepts, italicizing emphasis, and using monospaced text for component names and code
        snippets.

        Args:
            request (str): The user's query or request.
            content (str): The relevant documentation data to assist in generating the response.

        Returns:
            str: The generated response text formatted for Telegram.
        """
        prompt = f"""
            You are an expert assistant for the V4Fire framework, designed to help users by analysing relevant documentation content.

            Answer questions using retrieved documentation data.
            If user's question or ask is not related to V4Fire framework or if provided documents is not enough to answer the question, politely refuse to answer it!
            Explain features clearly, offering examples when relevant.
            Reference to the link to documentation for further details if link provided in context (do not mention references if link does not provided), and avoid jargon unless explained.
            Answer concisely. Do not provide extra explanation if not asked.

            Format the responses for Telegram using the following syntax in your response:
            1. Bold important concepts like subheaders using single asterisks: *text*
            2. Italicize emphasis using single underscore: _text_
            3. Use monospaced text for names of components: `text`
            4. Use multiline monospaced text for code snippets: ```text```
            5. To escape characters '_', '*', '`', '[' outside of an entity, prepend the characters '\\' before them.
            6. Entities must not be nested!! For example, text cannot be bold and monospaced at the same time!
            7. Do not make indents from line beginning for text in code snippets.
            You are not allowed to use any other formattings.

            User request: {request}

            Relevant documentation data:
            {content}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(e)
            return self.get_response(request=request, content=content)
    
    def get_summary(self, content: str):
        try:
            time.sleep(10)
            prompt = f"Summarize the following text: {content}"
            response = self.model.generate_content(prompt, request_options={'retry': retry.Retry()})
            return response.text
        except Exception as e:
            print(e)
            return self.get_summary(content)
        
    def generate_qa(self, content: str):
        try:
            time.sleep(10)
            prompt = f"""Generate question based on content provided and answer it as you think is th most correct based on the content.
            The content is a part of documentation V4Fire framework.
            Question is desired to be practically oriented or about some explanation.

            You must respond with json structure looking like that:
            {{
                "question": "generated question",
                "answer": "generated answer",
            }}
            Return ONLY that json structure!

            Content: {content}
            """
            response = self.model.generate_content(prompt, request_options={'retry': retry.Retry()})
            return response.text
        except Exception as e:
            print(e)
            return self.get_summary(content)

