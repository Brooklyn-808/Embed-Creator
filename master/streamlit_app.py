import streamlit as st
import json

# Initial setup for the page
st.title("Discord Embed Generator")
st.write(
    "Create, preview, and export your Discord embeds easily. Customize each embed and generate a JSON string to use in your bot."
)

# Store embed data
if "embeds" not in st.session_state:
    st.session_state.embeds = []

# Add a new embed section
if st.button("Add New Embed"):
    st.session_state.embeds.append({
        "title": "", "description": "", "color": "", "fields": [], "footer": "", "author": ""
    })
    st.rerun()  # Refresh the page to display new embed section

# Display instructions
st.subheader("Instructions")
st.write(
    "1. Customize your embeds below by adding titles, descriptions, colors, authors, and footers."
)
st.write(
    "2. Add fields to each embed if needed (e.g., additional info in the embed)."
)
st.write(
    "3. Once you're happy with the embeds, click 'Generate Embed Data JSON' to create the JSON string."
)

# Display embed inputs
for index, embed in enumerate(st.session_state.embeds):
    with st.expander(f"Embed {index + 1}", expanded=True):
        st.text_input(f"Title {index + 1}", value=embed["title"], key=f"title_{index}")
        st.text_area(f"Description {index + 1}", value=embed["description"], key=f"desc_{index}")
        st.color_picker(f"Color {index + 1}", value=embed["color"] or "#FFFFFF", key=f"color_{index}")
        st.text_input(f"Footer {index + 1}", value=embed["footer"], key=f"footer_{index}")
        st.text_input(f"Author {index + 1}", value=embed["author"], key=f"author_{index}")

        # Handle fields
        if "fields" not in st.session_state.embeds[index]:
            st.session_state.embeds[index]["fields"] = []

        st.write("Fields:")
        if st.button(f"Add Field to Embed {index + 1}"):
            st.session_state.embeds[index]["fields"].append({"name": "", "value": "", "inline": False})
            st.rerun()  # Refresh the page to show added field

        for field_index, field in enumerate(st.session_state.embeds[index]["fields"]):
            st.text_input(f"Field Name {field_index + 1}", value=field["name"], key=f"field_name_{index}_{field_index}")
            st.text_area(f"Field Value {field_index + 1}", value=field["value"], key=f"field_value_{index}_{field_index}")
            st.checkbox(f"Inline for Field {field_index + 1}", value=field["inline"], key=f"field_inline_{index}_{field_index}")

# Generate JSON string for embeds
if st.button("Generate Embed Data JSON"):
    embed_data = [
        {
            "title": embed["title"],
            "description": embed["description"],
            "color": embed["color"],
            "footer": embed["footer"],
            "author": embed["author"],
            "fields": [
                {
                    "name": field["name"],
                    "value": field["value"],
                    "inline": field["inline"]
                }
                for field in embed["fields"]
            ]
        }
        for embed in st.session_state.embeds if embed["title"] or embed["description"]
    ]

    embed_data_json = json.dumps(embed_data, indent=2)

    st.subheader("Generated Embed JSON")
    st.text_area("Embed Data JSON String", value=embed_data_json, height=300)
    st.write("Copy this JSON string and input it into your Disnake cog.")

    # Download button for the JSON
    st.download_button(
        label="Download Embed JSON",
        data=embed_data_json,
        file_name="discord_embeds.json",
        mime="application/json"
    )
