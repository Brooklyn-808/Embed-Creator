import streamlit as st
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = "http://212.192.29.158:25200"
API_KEY = os.getenv("MAY")

def fetch_channels():
    try:
        response = requests.get(f"{API_URL}/get_channels", params={"api_key": API_KEY})
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch channels. Check API key or server.")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching channels: {e}")
        return {}

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Soul Knight Prequel Discord Embed Generator",
    page_icon="https://cdn.discordapp.com/emojis/1250132570864091171.png",
)
st.title("Soul Knight Prequel Discord Embed Generator")
st.write("Create, preview, and export your Discord embeds easily. Customize each embed and generate a JSON string")

# Fetch channels
channels = fetch_channels()
channel_names = list(channels.keys()) if channels else ["No channels available"]
selected_channel = st.selectbox("Select a Discord Channel", channel_names)

# Store embed data in session state
if "embeds" not in st.session_state:
    st.session_state.embeds = []

# Add a new embed section
if st.button("Add New Embed"):
    st.session_state.embeds.append({
        "title": "", "description": "", "color": "#FFFFFF",
        "fields": [], "footer": {"text": "", "icon_url": ""},
        "author": {"name": "", "icon_url": ""},
        "image": None, "thumbnail": None
    })

# Embed customization interface
for index, embed in enumerate(st.session_state.embeds):
    with st.expander(f"Embed {index + 1}", expanded=True):
        embed["title"] = st.text_input(f"Title for Embed {index + 1}", value=embed["title"], key=f"title_{index}")
        embed["description"] = st.text_area(f"Description for Embed {index + 1}", value=embed["description"], key=f"desc_{index}")
        embed["color"] = st.color_picker(f"Color for Embed {index + 1}", value=embed["color"], key=f"color_{index}")
        embed["footer"]["text"] = st.text_input(f"Footer for Embed {index + 1}", value=embed["footer"].get("text", ""), key=f"footer_{index}")
        embed["footer"]["icon_url"] = st.text_input(f"Footer Icon URL for Embed {index + 1}", value=embed["footer"].get("icon_url", ""), key=f"footer_icon_{index}")
        embed["author"]["name"] = st.text_input(f"Author for Embed {index + 1}", value=embed["author"].get("name", ""), key=f"author_{index}")
        embed["author"]["icon_url"] = st.text_input(f"Author Icon URL for Embed {index + 1}", value=embed["author"].get("icon_url", ""), key=f"author_icon_{index}")
        embed["image"] = st.text_input(f"Image URL for Embed {index + 1}", value=embed.get("image", ""), key=f"image_{index}")
        embed["thumbnail"] = st.text_input(f"Thumbnail URL for Embed {index + 1}", value=embed.get("thumbnail", ""), key=f"thumbnail_{index}")

        if "fields" not in embed:
            embed["fields"] = []

        st.write("Fields:")
        if st.button(f"Add Field to Embed {index + 1}", key=f"add_field_{index}"):
            embed["fields"].append({"name": "", "value": "", "inline": False})
            st.rerun()

        for field_index, field in enumerate(embed["fields"]):
            field["name"] = st.text_input(f"Field Name for Field {field_index + 1} of Embed {index + 1}", value=field["name"], key=f"field_name_{index}_{field_index}")
            field["value"] = st.text_area(f"Field Value for Field {field_index + 1} of Embed {index + 1}", value=field["value"], key=f"field_value_{index}_{field_index}")
            field["inline"] = st.checkbox(f"Inline for Field {field_index + 1} of Embed {index + 1}", value=field["inline"], key=f"field_inline_{index}_{field_index}")

            if st.button(f"Remove Field {field_index + 1} from Embed {index + 1}", key=f"remove_field_{index}_{field_index}"):
                embed["fields"].pop(field_index)
                st.rerun()

        if st.button(f"Remove Embed {index + 1}", key=f"remove_embed_{index}"):
            st.session_state.embeds.pop(index)
            st.rerun()

# Generate JSON string
if st.button("Generate Embed Data JSON"):
    embed_data = [
        {
            "title": embed["title"],
            "description": embed["description"],
            "color": embed["color"],
            "footer": {"text": embed["footer"].get("text", ""), "icon_url": embed["footer"].get("icon_url", "")},
            "author": {"name": embed["author"].get("name", ""), "icon_url": embed["author"].get("icon_url", "")},
            "image": {"url": embed["image"]} if embed["image"] else None,
            "thumbnail": {"url": embed["thumbnail"]} if embed["thumbnail"] else None,
            "fields": [{"name": field["name"], "value": field["value"], "inline": field["inline"]} for field in embed["fields"]]
        }
        for embed in st.session_state.embeds if embed["title"] or embed["description"]
    ]

    embed_data_json = json.dumps(embed_data, indent=2)
    st.subheader("Generated Embed JSON")
    st.text_area("Embed Data JSON String", value=embed_data_json, height=300)
    st.download_button("Download Embed JSON", data=embed_data_json, file_name="discord_embeds.json", mime="application/json")

# Preview Embed button
if st.button("Preview Embed"):
    st.markdown("### Embed Preview")
    for embed in st.session_state.embeds:
        icon_ur = f"""<img src='{embed['author'].get('icon_url', '')}' style='width: 20px; height: 20px; border-radius: 50%; margin-right: 8px;'>""" if embed['author'].get('icon_url') else ""
        ficon_ur = f"""<img src='{embed['footer'].get('icon_url', '')}' style='width: 20px; height: 20px; border-radius: 50%; margin-right: 8px;'>""" if embed['footer'].get('icon_url') else ""
        color_style = f"border-left: 5px solid {embed['color']};" if embed['color'] else ""
        author_html = f"<div>{icon_ur} {embed['author'].get('name', '')}</div>" if embed['author'].get('name') else ""
        image_html = f"<img src='{embed['image']}' style='max-width: 100%; max-height: 300px; border-radius: 4px; margin-top: 8px;'>" if embed['image'] else ""
        thumbnail_html = f"<img src='{embed['thumbnail']}' style='width: 80px; height: 80px; border-radius: 4px; float: right;'>" if embed['thumbnail'] else ""
        footer_html = f"<div style='font-size: 10px; color: #b9bbbe;'>{ficon_ur} {embed['footer'].get('text', '')}</div>" if embed['footer'].get('text') else ""
        description_html = f"<div style='font-size: 14px; word-wrap: break-word; color: #b9bbbe;'>{embed['description']}</div>"
    
        fields_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">' + "".join([f"<div style='flex: 1; min-width: 45%; margin-top: 8px; border-top: 1px solid #b9bbbe; padding-top: 4px;'><strong>{field['name']}</strong><br>{field['value']}</div>" if field["inline"] else f"<div style='width: 100%; margin-top: 8px; border-top: 1px solid #b9bbbe; padding-top: 4px;'><strong>{field['name']}</strong><br>{field['value']}</div>" for field in embed["fields"]]) + "</div>"

    
        html_content = f"<div style='background-color: #36393f; padding: 16px; border-radius: 8px; color: white; {color_style} margin-bottom: 20px;'>{thumbnail_html}<div>{author_html}<div style='font-size: 18px; font-weight: bold;'>{embed['title']}</div>{description_html}{fields_html}{image_html}{footer_html}</div></div>"

    
        st.markdown(html_content, unsafe_allow_html=True)

# Send Embed button (send to selected channel)
if st.button("Send Embed"):
    if selected_channel != "No channels available" and st.session_state.embeds:
        embed_data = [
            {
                "title": embed["title"],
                "description": embed["description"],
                "color": embed["color"],
                "footer": {"text": embed["footer"].get("text", ""), "icon_url": embed["footer"].get("icon_url", "")},
                "author": {"name": embed["author"].get("name", ""), "icon_url": embed["author"].get("icon_url", "")},
                "image": {"url": embed["image"]} if embed["image"] else None,
                "thumbnail": {"url": embed["thumbnail"]} if embed["thumbnail"] else None,
                "fields": [{"name": field["name"], "value": field["value"], "inline": field["inline"]} for field in embed["fields"]]
            }
            for embed in st.session_state.embeds if embed["title"] or embed["description"]
        ]

        embed_payload = {
            "channel": selected_channel,
            "embeds": embed_data
        }

        try:
            response = requests.post(f"{API_URL}/send_embed", json=embed_payload)
            if response.status_code == 200:
                st.success("Embed sent successfully!")
            else:
                st.error(f"Failed to send embed. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error sending embed: {e}")
    else:
        st.error("Please select a channel and create at least one embed before sending.")

