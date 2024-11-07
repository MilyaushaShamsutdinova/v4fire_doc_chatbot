import google.generativeai as genai
from dotenv import load_dotenv
import os
import time


class GeminiAI:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
    def get_response(self, request, content):
        time.sleep(5)
        prompt = f"""
            You are an expert assistant for the V4Fire framework, designed to help users by analysing relevant documentation content.

            Answer questions using retrieved documentation data.
            If an exact match isn't found, provide general guidance and suggest related sections.
            Explain features clearly, offering examples when relevant.
            Keep responses concise, link to documentation for further details, and avoid jargon unless explained.

            User request: {request}

            Relevant documentation data:
            {content}
        """
        response = self.model.generate_content(prompt)
        return response.text
