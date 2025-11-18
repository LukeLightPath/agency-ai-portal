import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# --- Video Library ---
TUTORIAL_VIDEOS = {
    "AI Prospecting Assistant": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE", 
    "Image Prompt Analyzer": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE",
}

# --- Configuration ---
st.set_page_config(page_title="Agency AI Portal", layout="centered")
st.title("🤖 Agency AI Tools Portal")

# --- Sidebar for API Key ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input(
        "Enter Gemini API Key", 
        type="password",
        help="Get your key from Google AI Studio"
    )
    if api_key:
        st.success("API Key set!")
    else:
        st.warning("Please enter your Gemini API Key.")

# --- FUNCTION: Prospecting Tool ---
def generate_prospect_analysis(api_key, company_name, target_role, raw_signals, industry_trend):
    if not api_key: return "Error: API Key missing."
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        Analyze this prospect:
        Company: {company_name} | Role: {target_role}
        Signals: {raw_signals} | Trend: {industry_trend}
        
        Generate:
        1. Primary Pain Point
        2. Strategic Angle
        3. 3 Personalized Talking Points
        """
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return response.text
    except Exception as e: return f"Error: {e}"

# --- FUNCTION: Image Prompt Analyzer ---
def generate_image_prompt(api_key, uploaded_file):
    if not api_key: return "Error: API Key missing."
    try:
        client = genai.Client(api_key=api_key)
        image = Image.open(uploaded_file)
        prompt = "Analyze this image. Generate a detailed text prompt to recreate it using AI image generators. Structure: Subject, Style, Lighting/Camera."
        response = client.models.generate_content(model='gemini-2.0-flash', contents=[image, prompt])
        return response.text
    except Exception as e: return f"Error: {e}"

# --- MAIN NAVIGATION ---
tool_choice = st.radio("Select a Tool:", ["AI Prospecting Assistant", "Image Prompt Analyzer"], horizontal=True)

st.divider()

# --- UI: AI Prospecting Assistant ---
if tool_choice == "AI Prospecting Assistant":
    st.header("🔎 AI Prospecting Assistant")
    
    tab1, tab2 = st.tabs(["🚀 Launch Tool", "📚 Tutorial"])
    
    with tab2:
        st.video(TUTORIAL_VIDEOS["AI Prospecting Assistant"])
    
    with tab1:
        with st.form("prospect_form"):
            c1, c2 = st.columns(2)
            company = c1.text_input("Company Name")
            role = c2.text_input("Target Role")
            signals = st.text_area("Recent News/Signals")
            trend = st.text_area("Industry Trend")
            submitted = st.form_submit_button("Generate Strategy")
            
            if submitted:
                with st.spinner("Analyzing..."):
                    res = generate_prospect_analysis(api_key, company, role, signals, trend)
                    st.markdown(res)

# --- UI: Image Prompt Analyzer ---
elif tool_choice == "Image Prompt Analyzer":
    st.header("🖼️ Image Prompt Analyzer")
    
    tab1, tab2 = st.tabs(["🚀 Launch Tool", "📚 Tutorial"])
    
    with tab2:
        st.video(TUTORIAL_VIDEOS["Image Prompt Analyzer"])
        
    with tab1:
        up_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if up_file and st.button("Analyze Image"):
             with st.spinner("Analyzing..."):
                 res = generate_image_prompt(api_key, up_file)
                 st.image(up_file, width=200)
                 st.code(res)