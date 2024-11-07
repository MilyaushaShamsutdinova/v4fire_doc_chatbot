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

            Format the responses for Telegram using these rules:
            1. Bold important concepts like subheaders using double asterisks: **text**
            2. Italicize emphasis using one asterisks: *text*
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
