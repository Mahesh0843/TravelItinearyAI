# # services/call_llm.py
# import google.generativeai as genai
# import streamlit as st

# @st.cache_resource
# def _get_model():
#     genai.configure(api_key=st.secrets["gemini_api_key"])
#     return genai.GenerativeModel("gemini-3-flash-preview")

# def ask_gemini(prompt):
#     try:
#         model = _get_model()
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         st.error(f"Gemini API error: {e}")
#         return None

# services/call_llm.py
import google.genai as genai
import streamlit as st

def ask_gemini(prompt):
    try:
        print("🔍 DEBUG: Starting Gemini API call...")
        client = genai.Client(api_key=st.secrets["gemini_api_key"])
        print("✅ DEBUG: Client created successfully")
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        print("✅ DEBUG: API response received")
        return response.text
    except Exception as e:
        print(f"❌ DEBUG: Gemini API error: {e}")
        st.error(f"Gemini API error: {e}")
        return None
