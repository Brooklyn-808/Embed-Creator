import streamlit as st
import json

# Initial setup for the page
st.title("Soul Knight Prequel Discord Embed Generator")
st.write(
    "Create, preview, and export your Discord embeds easily. Customize each embed and generate a JSON string"
)

# Store embed data in session state
if "embeds" not in st.session_state:
    st.session_state.embeds = []

# Add a new embed section
if st.button("Add New Embed"):
    st.session_state.embeds.append({
        "title": "", "description": "", "color": "", "fields": [], "footer": "", "author": "", "image": None, "thumbnail": None
    })

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

# Old JSON input box for users to paste
st.subheader("Or paste your previous JSON below:")
old_json = st.text_area("Paste old JSON here:", height=200, key="old_json_input")

# If user provides JSON, try to load it into the session state only if no embeds are already in session state
if old_json and not st.session_state.embeds:
    try:
        embed_data = json.loads(old_json)
        st.session_state.embeds = embed_data
        st.write("Loaded your previous JSON successfully!")
    except json.JSONDecodeError:
        st.write("Invalid JSON format. Please paste a valid JSON.")

# Display embed inputs for all current embeds
for index, embed in enumerate(st.session_state.embeds):
    with st.expander(f"Embed {index + 1}", expanded=True):
        # Update embed data
        embed["title"] = st.text_input(f"Title for Embed {index + 1}", value=embed["title"], key=f"title_{index}")
        embed["description"] = st.text_area(f"Description for Embed {index + 1}", value=embed["description"], key=f"desc_{index}")
        embed["color"] = st.color_picker(f"Color for Embed {index + 1}", value=embed["color"] or "#FFFFFF", key=f"color_{index}")
        embed["footer"] = st.text_input(f"Footer for Embed {index + 1}", value=embed["footer"], key=f"footer_{index}")
        embed["author"] = st.text_input(f"Author for Embed {index + 1}", value=embed["author"], key=f"author_{index}")
        
        # Image and Thumbnail URL fields
        embed["image"] = st.text_input(f"Image URL for Embed {index + 1}", value=embed.get("image", ""), key=f"image_{index}")
        embed["thumbnail"] = st.text_input(f"Thumbnail URL for Embed {index + 1}", value=embed.get("thumbnail", ""), key=f"thumbnail_{index}")

        # Handle fields
        if "fields" not in embed:
            embed["fields"] = []

        st.write("Fields:")
        if st.button(f"Add Field to Embed {index + 1}", key=f"add_field_{index}"):
            embed["fields"].append({"name": "", "value": "", "inline": False})
            st.session_state.embeds = st.session_state.embeds  # To trigger the rerun
            st.experimental_rerun()  # Refresh the page to show added field

        for field_index, field in enumerate(embed["fields"]):
            field["name"] = st.text_input(f"Field Name for Field {field_index + 1} of Embed {index + 1}", value=field["name"], key=f"field_name_{index}_{field_index}")
            field["value"] = st.text_area(f"Field Value for Field {field_index + 1} of Embed {index + 1}", value=field["value"], key=f"field_value_{index}_{field_index}")
            field["inline"] = st.checkbox(f"Inline for Field {field_index + 1} of Embed {index + 1}", value=field["inline"], key=f"field_inline_{index}_{field_index}")

# Generate JSON string for embeds
if st.button("Generate Embed Data JSON"):
    embed_data = [
        {
            "title": embed["title"],
            "description": embed["description"],
            "color": embed["color"],
            "footer": embed["footer"],
            "author": embed["author"],
            "image": {
                "url": embed["image"]
            } if embed["image"] else None,
            "thumbnail": {
                "url": embed["thumbnail"]
            } if embed["thumbnail"] else None,
            "fields": [
                {
                    "name": field["name"],
                    "value": field["value"],
                    "inline": field["inline"]
                }
                for field in embed["fields"]
            ]
        }
        for embed in st.session_state.embeds if embed["title"] or embed["description"]  # Include even if fields are empty
    ]

    embed_data_json = json.dumps(embed_data, indent=2)

    st.subheader("Generated Embed JSON")
    st.text_area("Embed Data JSON String", value=embed_data_json, height=300)
    st.write("Copy this JSON string and send it as >>send_embed <json string>")

    # Download button for the JSON
    st.download_button(
        label="Download Embed JSON",
        data=embed_data_json,
        file_name="discord_embeds.json",
        mime="application/json"
    )
