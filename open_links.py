import webbrowser
import pandas as pd
import os
import time
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Tkinter for file upload dialog
root = tk.Tk()
root.withdraw()

# Ask user to select an Excel file
file_path = filedialog.askopenfilename(
    title="Select an Excel File",
    filetypes=[("Excel Files", "*.xlsx;*.xls")]
)

# Check if the user selected a file
if not file_path:
    print("❌ No file selected. Exiting.")
    exit()

# Load the Excel file
df = pd.read_excel(file_path)

# Ensure 'Link' column exists
if "Link" not in df.columns:
    print("❌ Error: No 'Link' column found in the file.")
    exit()

# Extract links and clean them
links = df["Link"].dropna().tolist()

# Set up Chrome WebDriver with WebDriver Manager
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in the background
chrome_options.add_argument("--window-size=1280,800")  # Set window size

# Automatically download the right ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Create folder to save screenshots
screenshot_folder = "SocialMedia_Screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

# Open each link and take a screenshot
for idx, link in enumerate(links):
    if not link.startswith(("http://", "https://")):
        link = "https://" + link  # Ensure proper URL format
    
    print(f"📷 Taking screenshot of: {link}")
    
    driver.get(link)  # Open the link in Selenium
    time.sleep(5)  # Wait for page to load fully

    # Define screenshot file name
    screenshot_path = os.path.join(screenshot_folder, f"post_{idx+1}.png")

    # Take screenshot of full page
    driver.save_screenshot(screenshot_path)

    print(f"✅ Screenshot saved: {screenshot_path}")

# Close Selenium browser
driver.quit()

print(f"🎉 Screenshots saved in: {os.path.abspath(screenshot_folder)}")
