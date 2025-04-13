import streamlit as st
import random
import json
import google.generativeai as genai
import matplotlib.pyplot as plt
import os
import base64
import zlib

# ✅ Load Gemini API Key securely
GEMINI_API_KEY = "AIzaSyB8Ab3gXsAb9TXl38UeeJ9hMiH1c8dj--I"
if not GEMINI_API_KEY:
    st.error("API Key is missing. Please set the 'GEMINI_API_KEY' environment variable.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Load user profile from JSON
def load_user_profile(file_path="user_profile.json"):
    try:
        with open(file_path, "r") as file:
            profile_data = json.load(file)
        return profile_data
    except FileNotFoundError:
        st.error(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        st.error("Error decoding the JSON file.")
        return None

# ✅ Career Roadmap Generation
def generate_career_roadmap(profile_data):
    prompt = f"""
    You are a friendly career guide assistant.

    Generate a roadmap in friendly and structured format for the following user:

    👤 Name: {profile_data['name']}
    🎓 Education: {profile_data['education']}
    🛠️ Skills: {', '.join(profile_data['skills'])}
    📍 Experience: {profile_data['experience']}

    📚 Courses Completed:
    """
    for course in profile_data['courses']:
        prompt += f"- {course['course_name']} (Marks: {course['marks']}, Date: {course['date']})\n"

    prompt += """ 

    Now, do the following:

    1. Greet the user.
    2. Describe their education & give a positive/neutral assessment of it.
    3. Analyze their skills and tell if they are sufficient, average, or need improvement.
    4. Discuss the work experience, and optionally provide real-life quotes/examples where such experience is valued.
    5. Analyze completed courses and recommend 2–3 more relevant courses they can take.
    6. Suggest a personalized career path: job roles they can target, required skills/certifications, and industries.
    7. Give an approximate 6-month action plan with timelines.
    8. End with a motivational note.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating career roadmap: {e}")
        return "Sorry, there was an error generating your career roadmap."

# ✅ PlantUML Helpers for Flowchart
def deflate_and_encode(plantuml_text):
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return encode64(compressed_string)

def encode64(data):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    encoded = ""
    b = 0
    bits = 0
    for byte in data:
        b = (b << 8) | byte
        bits += 8
        while bits >= 6:
            bits -= 6
            encoded += alphabet[(b >> bits) & 0x3F]
    if bits > 0:
        encoded += alphabet[(b << (6 - bits)) & 0x3F]
    return encoded

# ✅ Tailoring and Jaggery Course Data
course_data = [
    {
        "user_input": "Learn Tailoring",
        "suggested_courses": [
            {
                "title": "Tailoring for Beginners - Full Course",
                "channel": "Fashion with Style",
                "duration": "8:30:00",
                "url": "https://www.youtube.com/watch?v=example_tailoring_course",
                "thumbnail": "https://i.ytimg.com/vi/example_tailoring_course/hqdefault.jpg"
            },
            {
                "title": "Basic Sewing Techniques - Tailoring Skills",
                "channel": "Learn Sewing with Jenny",
                "duration": "5:15:00",
                "url": "https://www.youtube.com/watch?v=example_sewing_skills",
                "thumbnail": "https://i.ytimg.com/vi/example_sewing_skills/hqdefault.jpg"
            }
        ]
    },
    {
        "user_input": "Learn Jaggery Making",
        "suggested_courses": [
            {
                "title": "How to Make Jaggery at Home",
                "channel": "Traditional Cooking with Ramesh",
                "duration": "3:45:00",
                "url": "https://www.youtube.com/watch?v=example_jaggery_course",
                "thumbnail": "https://i.ytimg.com/vi/example_jaggery_course/hqdefault.jpg"
            },
            {
                "title": "Jaggery Production and Benefits",
                "channel": "Ayurvedic Cooking with Shreya",
                "duration": "4:00:00",
                "url": "https://www.youtube.com/watch?v=example_jaggery_benefits",
                "thumbnail": "https://i.ytimg.com/vi/example_jaggery_benefits/hqdefault.jpg"
            }
        ]
    }
]

# ✅ Motivational Quotes
quotes = [
    "Believe in yourself – you are capable of amazing things.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Your journey is unique. Embrace it with pride!",
    "Dream big, start small, act now.",
    "Every expert was once a beginner."
]

# ✅ Streamlit Layout
st.set_page_config(page_title="Skill-based Course Recommendations & Career Roadmap", layout="wide")
st.sidebar.title("📂 Options")
st.sidebar.markdown("Use the options below to interact:")

show_roadmap = st.sidebar.checkbox("📌 Show Career Roadmap", value=True)
show_flowchart = st.sidebar.checkbox("📊 Show Career Flowchart", value=True)
show_course_recommendations = st.sidebar.checkbox("📚 Course Recommendations", value=True)
show_quote = st.sidebar.checkbox("💡 Quote of the Day", value=True)

# Load Profile (from JSON)
profile_data = load_user_profile()
if profile_data:
    st.title(f"🚀 Personalized Career Roadmap Generator for {profile_data['name']}")
    st.success(f"Profile loaded for **{profile_data['name']}**")
else:
    st.error("Unable to load the user profile.")

# ✅ Course Recommendation
if show_course_recommendations:
    st.subheader("📚 Skill-based Course Recommendations")
    skill_input = st.text_input("Enter the skill you want to learn (e.g., 'Learn skills'): ")

    if skill_input:
        skill_match = next((item["suggested_courses"] for item in course_data if item["user_input"].lower() == skill_input.lower()), None)
        if skill_match:
            for course in skill_match:
                st.markdown(f"**{course['title']}**  ")
                st.markdown(f"*Channel:* {course['channel']}  ")
                st.markdown(f"*Duration:* {course['duration']}  ")
                st.markdown(f"[Watch Now]({course['url']})")
                st.image(course['thumbnail'])
        else:
            st.warning("No recommendations found for the entered skill. Please try again.")

# ✅ Career Roadmap Display
if show_roadmap and profile_data:
    with st.spinner("Generating your personalized roadmap..."):
        roadmap_text = generate_career_roadmap(profile_data)

    st.markdown("## 🎯 Your Career Roadmap")
    st.markdown(roadmap_text)

    file_name = f"career_roadmap_for_{profile_data['name'].replace(' ', '_')}.txt"
    st.download_button("📄 Download Roadmap", roadmap_text, file_name, mime="text/plain")

# ✅ Career Flowchart
if show_flowchart:
    plantuml_code = """
    @startuml
    skinparam backgroundColor #FFFFFF
    skinparam defaultFontSize 14
    skinparam node {
        BackgroundColor white
        BorderColor black
        FontSize 14
    }
    skinparam ArrowColor #4B8BBE

    title Career Roadmap - Month-wise 🎯

start
:📚 Jan: Informal Education\nDropped Out After 10th Grade;
note right
"You are here"
end note
:🧶 Feb: Skill Discovery\nTailoring, Handicrafts, Basic Caregiving (from home & workshops);
:🎥 Mar: Online Learning\nMobile App + NGO Courses (Spoken English, Computer Basics);
:💻 Apr: Hands-on Practice\nTailoring for Neighbors, Helping at Local Clinic;
:👩‍👧 May: Community Help\nAssisted Women in Learning Tailoring Basics;
:🎓 Jun: Upskilling\nCompleted Computer & Handicrafts Course;
:📱 Jul: Digital Presence\nWhatsApp Catalog, Basic Phone Skills;
:🎨 Aug: Expand Skills\nFabric Handling, Finishing Techniques;

split
    :🚀 Path 1:\nHospital Attendant Role\n(Sept - Apply Locally);
split again
    :🪡 Path 2:\nPart-time Tailoring Work\n(Home or Boutique-based);
split again
    :🧑‍🏫 Path 3:\nCommunity Trainer\nTeach Women Basic Skills;
split again
    :🛍️ Path 4:\nSell Handicrafts & Clothes\nOnline/Offline;
endsplit

:🧳 Oct: Portfolio Prep\nClick Work Photos, Create WhatsApp Showcase;
:📢 Nov-Dec: Promotion Time\nLeaflets, Local WhatsApp Groups, Community Events;
stop
@enduml

    """
    encoded = deflate_and_encode(plantuml_code)
    plantuml_url = f"http://www.plantuml.com/plantuml/png/{encoded}"

    st.subheader("🌐 Visual Career Map (PlantUML)")
    st.image(plantuml_url, caption="Branched Career Journey Diagram")

# ✅ Motivational Quote
if show_quote:
    st.subheader("💡 Motivational Quote")
    random_quote = random.choice(quotes)
    st.markdown(f"**{random_quote}**")