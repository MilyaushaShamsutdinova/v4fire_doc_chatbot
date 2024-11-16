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
        # time.sleep(5)
        prompt = f"""
            You are an expert assistant for the V4Fire framework, designed to help users by analysing relevant documentation content.

            Answer questions using retrieved documentation data.
            If user's question or ask is not related to V4Fire framework or if provided documents is not enough to answer the question, politely refuse to answer it!
            Explain features clearly, offering examples when relevant.
            Keep responses concise, link to documentation for further details, and avoid jargon unless explained.

            Format the responses for Telegram using these rules:
            1. Bold important concepts like subheaders using double asterisks: **text**
            2. Italicize emphasis using double underscore: __text__
            3. Use monospaced text for names of components: `text`
            4. Use multiline monospaced text for code snippets: ```text```
            5. Do not combine formatting functions!! For example, text cannot be bold and monospaced at the same time!
            6. Do not make indents from line beginning for text in code snippets.
            You are not allowed to use any other formattings.

            User request: {request}

            Relevant documentation data:
            {content}
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    def get_summary(self, content: str):
        try:
            time.sleep(10)
            prompt = f"Summarize the following text: {content}"
            response = self.model.generate_content(prompt, request_options={'retry': retry.Retry()})
            # print("---", response.text[:150])
            return response.text
        except Exception as e:
            print(e)
            return self.get_summary(content)

