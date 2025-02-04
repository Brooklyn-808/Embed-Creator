
import streamlit as st
import json

# Initial setup for page
st.title("Discord Embed Generator")
st.write("Easily create and export infinite Discord embeds as a JSON string.")

# Store embed data
if "embeds" not in st.session_state:
    st.session_state.embeds = []

# Add a new embed section
if st.button("Add New Embed"):
    st.session_state.embeds.append({"title": "", "description": "", "color": ""})

# Display embed inputs
for index, embed in enumerate(st.session_state.embeds):
    st.subheader(f"Embed {index + 1}")
    st.session_state.embeds[index]["title"] = st.text_input(f"Title {index + 1}", value=embed["title"], key=f"title_{index}")
    st.session_state.embeds[index]["description"] = st.text_area(f"Description {index + 1}", value=embed["description"], key=f"desc_{index}")
    st.session_state.embeds[index]["color"] = st.color_picker(f"Color {index + 1}", value=embed["color"] or "#FFFFFF", key=f"color_{index}")

# Generate JSON string for embeds
if st.button("Generate Embed Data JSON"):
    embed_data = [
        {
            "title": embed["title"],
            "description": embed["description"],
            "color": embed["color"]
        }
        for embed in st.session_state.embeds if embed["title"] or embed["description"]
    ]

    embed_data_json = json.dumps(embed_data, indent=2)

    st.text_area("Embed Data JSON String", value=embed_data_json, height=200)
    st.write("Copy this JSON string and input it into your Disnake cog.")
