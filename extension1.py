from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# === Facebook credentials ===
FB_EMAIL = "your_email_here"
FB_PASSWORD = "your_pass_here"

# === Setup Chrome ===
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.facebook.com/")
time.sleep(15)

# === Login ===
email_box = driver.find_element(By.ID, "email")
password_box = driver.find_element(By.ID, "pass")
email_box.send_keys(FB_EMAIL)
password_box.send_keys(FB_PASSWORD)
password_box.send_keys(Keys.RETURN)
print("🔑 Login submitted...")
time.sleep(30)  # wait for login to complete

# === Go to Friends List Page ===
driver.get("https://www.facebook.com/friends/list")
time.sleep(8)

# === Scroll to load all friends ===
print("⏳ Scrolling to load all friends...")
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
print("✅ All friends loaded")

# === Extract friends names + URLs ===
friend_elements = driver.find_elements(By.XPATH, "//a[@role='link' and contains(@href,'facebook.com')]")
friends_set = set()
friends_data = []

for f in friend_elements:
    try:
        name_span = f.find_element(By.XPATH, ".//span")
        name = name_span.text.strip()
        url = f.get_attribute("href")

        if name and url and url not in friends_set:
            friends_set.add(url)
            friends_data.append({"Name": name, "Profile URL": url})
    except:
        continue

print(f"✅ Extracted {len(friends_data)} unique friends")

# === Save friends list to CSV ===
with open("friends_list.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Profile URL"])
    writer.writeheader()
    writer.writerows(friends_data)


print("✅ Friends list saved to friends_list.csv")
driver.quit()

