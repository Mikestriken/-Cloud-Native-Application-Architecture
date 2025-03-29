import streamlit as st
import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line %(lineno)d - %(message)s'
)

# Create a logger instance (optional if using root logger)
logger = logging.getLogger(__name__)

# Example usage
def test_logging():
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

BASE_URL = "http://127.0.0.1:8000" # Local FastAPI server
st.title("Streamlit-FastAPI Demo")

st.header("Get an Item by ID")
item_id = st.number_input("Item ID", min_value=1, value=1, step=1)

if st.button("Get Item"):
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to retrieve item")

st.header("Create a New Item")
item_name = st.text_input("Name")
item_desc = st.text_input("Description")
item_price = st.number_input("Price", min_value=0.0, value=0.0, step=0.01)

if st.button("Create Item"):
    payload = {
    "name": item_name,
    "description": item_desc,
    "price": item_price
    }
    
    response = requests.post(f"{BASE_URL}/items/", json=payload)
    
    if response.status_code == 200:
        st.success("Item created successfully!")
        st.json(response.json())
    else:
        st.error("Failed to create item")