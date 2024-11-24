import streamlit as st
import json

# Load JSON data
TICKER = 'AAPL'
with open(f'data/{TICKER}_summaries.json', 'r') as f:
    data = json.load(f)

st.title(f'{TICKER} Feed')

# Custom CSS for tile styling
st.markdown("""
    <style>
    .stApp {
        background-color: #1e3d59; /* dark blue */
    }
    
    .tile {
        background-color: #f5f5f5; /* light gray */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .tile p {
        font-size: 16px;
        color: #1e3d59; /* dark blue */
        margin: 0;
    }
    /* Remove underline and blue color from links */
    a {
        text-decoration: none;
        color: inherit;
    }
    </style>
    """, unsafe_allow_html=True)

# Display summaries as tiles
for item in data:
    st.markdown(f"""
    <a href="{item['link']}" target="_blank">
        <div class="tile">
            <p>{item['summary']}</p>
        </div>
    </a>
    """, unsafe_allow_html=True)