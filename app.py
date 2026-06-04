import streamlit as st
from openai import OpenAI

# Initialize OpenAI Client (Uses Streamlit secrets safely)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 K-Drama Eyewear Matcher for Lenskart")
st.write("Type a K-Drama or character name to find matching frames!")

user_query = st.text_input("Example: Show me the glasses worn by Hong Hae-in in Queen of Tears")

if user_query:
    with st.spinner("Analyzing pop culture data..."):
        # Step 1: Ask the LLM to identify the frame features based on its internal knowledge base
        system_prompt = (
            "You are a K-Drama fashion expert. Analyze the user's request. "
            "Identify the style of glasses worn by that character. Output ONLY a clean JSON object "
            "with these exact keys: 'shape' (choose from: round, rectangle, square, aviator, cat-eye), "
            "'material' (choose from: metal, acetate, acetate-metal), and 'color' (one word color). "
            "Do not include markdown or backticks."
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )
        
        try:
            # Parse the AI response
            import json
            specs = json.loads(response.choices[0].message.content.strip())
            
            st.subheader("📌 Detected Style Profile:")
            st.write(f"**Shape:** {specs['shape']} | **Material:** {specs['material']} | **Color:** {specs['color']}")
            
            # Step 2: Dynamically map the features to Lenskart's URL filter structure
            lenskart_url = f"https://www.lenskart.com/eyeglasses/frame-shape/{specs['shape']}/frame-material/{specs['material']}.html?color={specs['color']}"
            
            # Alternative: If it sounds like modern K-Style, link to their dedicated K-Pop collection
            kpop_collection_url = "https://www.lenskart.com/eyewear/promotion/kpop.html"
            
            st.success("We found matching styles!")
            st.markdown(f"👉 [**Click here to view live matches on Lenskart**]({lenskart_url})")
            st.markdown(f"🌟 Or browse the curated [**Official Lenskart Studio K-Pop Collection**]({kpop_collection_url})")
            
        except Exception as e:
            st.error("Could not parse the character's style. Try a different show or character name!")