import streamlit as st
import os
import pandas as pd
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to take screenshots
def take_screenshots(file_path):
    df = pd.read_excel(file_path)
    links = df["Link"].dropna().tolist()

    chrome_options = Options()
    chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    chrome_options.add_argument("user-data-dir=C:/Users/adswi/AppData/Local/Google/Chrome/User Data")
    chrome_options.add_argument("profile-directory=Default")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    screenshot_folder = "SocialMedia_Screenshots"
    os.makedirs(screenshot_folder, exist_ok=True)

    for idx, link in enumerate(links):
        driver.get(link)
        time.sleep(5)
        screenshot_path = os.path.join(screenshot_folder, f"post_{idx+1}.png")
        driver.save_screenshot(screenshot_path)
    
    driver.quit()

# Streamlit UI
st.title("Social Media Post Screenshot Tool")

uploaded_file = st.file_uploader("Upload Excel file with links", type=["xlsx"])
if uploaded_file is not None:
    file_path = os.path.join("temp.xlsx")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Run Selenium in a separate thread to avoid blocking Streamlit
    st.text("Taking screenshots in the background...")
    threading.Thread(target=take_screenshots, args=(file_path,)).start()

    # Show the screenshots when available
    screenshot_folder = "SocialMedia_Screenshots"
    if os.path.exists(screenshot_folder):
        for img in os.listdir(screenshot_folder):
            st.image(os.path.join(screenshot_folder, img))

st.text("Screenshots will appear here once captured.")
