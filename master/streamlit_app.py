import streamlit as st
import json

st.set_page_config(
    page_title="Soul Knight Prequel Discord Embed Generator",
    page_icon="https://cdn.discordapp.com/emojis/1250132570864091171.png",  # replace with your image URL
)
# Initial setup for the page
st.title("Soul Knight Prequel Discord Embed Generator")
st.write("Create, preview, and export your Discord embeds easily. Customize each embed and generate a JSON string")

# Store embed data in session state
if "embeds" not in st.session_state:
    st.session_state.embeds = []

# Add a new embed section
if st.button("Add New Embed"):
    st.session_state.embeds.append({
        "title": "", "description": "", "color": "", "fields": [], "footer": {"text": "", "icon_url": ""}, "author": {"name": "", "icon_url": ""}, "image": None, "thumbnail": None
    })

# Display instructions
st.subheader("Instructions")
st.write("1. Customize your embeds below by adding titles, descriptions, colors, authors, and footers.")
st.write("2. Add fields to each embed if needed (e.g., additional info in the embed).")
st.write("3. Once you're happy with the embeds, click 'Generate Embed Data JSON' to create the JSON string.")

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
        embed["footer"]["text"] = st.text_input(f"Footer for Embed {index + 1}", value=embed["footer"].get("text", ""), key=f"footer_{index}")
        embed["footer"]["icon_url"] = st.text_input(f"Footer Icon URL for Embed {index + 1}", value=embed["footer"].get("icon_url", ""), key=f"footer_icon_{index}")
        embed["author"]["name"] = st.text_input(f"Author for Embed {index + 1}", value=embed["author"].get("name", ""), key=f"author_{index}")
        embed["author"]["icon_url"] = st.text_input(f"Author Icon URL for Embed {index + 1}", value=embed["author"].get("icon_url", ""), key=f"author_icon_{index}")

        # Image and Thumbnail URL fields
        embed["image"] = st.text_input(f"Image URL for Embed {index + 1}", value=embed.get("image", ""), key=f"image_{index}")
        embed["thumbnail"] = st.text_input(f"Thumbnail URL for Embed {index + 1}", value=embed.get("thumbnail", ""), key=f"thumbnail_{index}")

        # Handle fields
        if "fields" not in embed:
            embed["fields"] = []

        st.write("Fields:")
        if st.button(f"Add Field to Embed {index + 1}", key=f"add_field_{index}"):
            embed["fields"].append({"name": "", "value": "", "inline": False})
            st.rerun()  # Refresh the page to show added field

        for field_index, field in enumerate(embed["fields"]):
            field["name"] = st.text_input(f"Field Name for Field {field_index + 1} of Embed {index + 1}", value=field["name"], key=f"field_name_{index}_{field_index}")
            field["value"] = st.text_area(f"Field Value for Field {field_index + 1} of Embed {index + 1}", value=field["value"], key=f"field_value_{index}_{field_index}")
            field["inline"] = st.checkbox(f"Inline for Field {field_index + 1} of Embed {index + 1}", value=field["inline"], key=f"field_inline_{index}_{field_index}")

            # Remove field button
            if st.button(f"Remove Field {field_index + 1} from Embed {index + 1}", key=f"remove_field_{index}_{field_index}"):
                embed["fields"].pop(field_index)
                st.rerun()

        # Remove embed button
        if st.button(f"Remove Embed {index + 1}", key=f"remove_embed_{index}"):
            st.session_state.embeds.pop(index)
            st.rerun()

# Generate JSON string for embeds
if st.button("Generate Embed Data JSON"):
    # Ensure the latest data is used
    embed_data = [
        {
            "title": embed["title"],
            "description": embed["description"],
            "color": embed["color"],
            "footer": {
                "text": embed["footer"].get("text", ""),
                "icon_url": embed["footer"].get("icon_url", "")
            },
            "author": {
                "name": embed["author"].get("name", ""),
                "icon_url": embed["author"].get("icon_url", "")
            },
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

# Embed HTML Preview Button
if st.button("Preview Embed"):
    st.markdown("### Embed Preview")
    for embed in st.session_state.embeds:
        if not embed['title']:
            st.warning("Embed is missing a title and cannot be previewed.")
            continue
        
        color_style = f"border-left: 5px solid {embed['color']};" if embed['color'] else ""
        author_html = f"<div><img src='{embed['author'].get('icon_url', '')}' alt='Author Icon' style='width: 20px; height: 20px; border-radius: 50%; margin-right: 8px; display: inline-block;'> {embed['author'].get('name', '')}</div>" if embed['author'].get('name') else ""
        image_html = f"<img src='{embed['image']}' style='max-width: 100%; max-height: 300px; border-radius: 4px; margin-top: 8px;'>" if embed['image'] else ""
        thumbnail_html = f"<img src='{embed['thumbnail']}' style='width: 80px; height: 80px; border-radius: 4px; margin-left: 16px; float: right;'>" if embed['thumbnail'] else ""
        footer_html = f"<div style='font-size: 10px; color: #b9bbbe;'>{embed['footer'].get('text', '')}</div>" if embed['footer'].get('text') else ""
        des_html = f"""<div style="font-size: 14px; color: #b9bbbe;">{embed['description']}</div>"""
        st.markdown(f"""<div style="background-color: #36393f; padding: 16px; border-radius: 8px; color: white; {color_style} margin-bottom: 20px;">{thumbnail_html}<div>{author_html}<div style="font-size: 18px; font-weight: bold;">{embed['title']}</div>{des_html}{image_html}{footer_html}</div></div>""", unsafe_allow_html=True)
