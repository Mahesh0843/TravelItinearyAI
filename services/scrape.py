# services/scrape.py
from google import genai
from google.genai import types
import streamlit as st
import json
import re

def get_rentals(location):
    # 1. Set up the Gemini client with your API key
    client = genai.Client(api_key=st.secrets["gemini_api_key"])

    # 2. Construct a detailed prompt for the model
    prompt = f"""
    Find the best self-drive car rentals in {location}.

    For the top 3 car rental providers, provide the following details:
    - name: Name of the company
    - type: The type of car (e.g., Hatchback, SUV)
    - price: The rental price for one day
    - phone: Contact number
    - map: The Google Maps link to their location

    Return ONLY the data as a valid JSON list. Do not include any other text, explanations, or formatting.
    """

    # 3. Make the API request, enabling Google Search
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )

    # 4. Extract and parse the JSON response
    response_text = response.text.strip()
    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
    
    if json_match:
        json_data = json_match.group(0)
        rentals = json.loads(json_data)
        return rentals
    else:
        print("No JSON data found in the response.")
        return []