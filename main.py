import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import base64

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["rishtaDB"]
collection = db["rishtay"]

st.title("💍 Rishta Timeline")

# Display Rishtay
st.header("Available Rishtay")
rishtay = collection.find()
for r in rishtay:
    with st.container():
        st.subheader(f"{r['name']} ({r['age']})")
        st.write(f"Gender: {r['gender']}")
        st.write(f"Location: {r['location']}")
        st.write(f"Bio: {r['bio']}")
        # Display image if exists
        if "image" in r:
            img_data = base64.b64decode(r["image"])
            st.image(img_data, width=400)  # limit width to 400 pixels
        st.markdown("---")

# Rishta Post Form
st.sidebar.header("📨 Post Your Rishta")

with st.sidebar.form("post_form", clear_on_submit=True):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=80)
    gender = st.selectbox("Gender", ["Male", "Female"])
    location = st.text_input("Location")
    bio = st.text_area("Short Bio")
    image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    submitted = st.form_submit_button("Post Rishta")

if submitted:
    img_base64 = None
    if image is not None:
        # Convert image to base64 string
        img_base64 = base64.b64encode(image.read()).decode()

    doc = {
        "name": name,
        "age": age,
        "gender": gender,
        "location": location,
        "bio": bio,
    }
    if img_base64:
        doc["image"] = img_base64

    collection.insert_one(doc)
    st.success("✅ Your rishta has been posted!")
