from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# === Your Facebook credentials ===
FB_EMAIL = "your_email_here"
FB_PASSWORD = "your_pass_here"

# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.facebook.com/")
time.sleep(10)

# Login
email_box = driver.find_element(By.ID, "email")
password_box = driver.find_element(By.ID, "pass")
email_box.send_keys(FB_EMAIL)
password_box.send_keys(FB_PASSWORD)
password_box.send_keys(Keys.RETURN)

print("Login submitted...")
time.sleep(20)

# Check login
if "facebook.com" not in driver.current_url:
    print("❌ Login failed.")
    driver.quit()
    exit()
print("✅ Logged in successfully!")

# === Navigate to profile ===
# Profile button is usually inside the top bar
driver.get("https://www.facebook.com/me")
time.sleep(10)

# === Click on Friends tab ===
try:
    friends_tab = driver.find_element(By.XPATH, "//a[contains(@href, '/friends')]")
    driver.get(friends_tab.get_attribute("href"))
    print("➡️ Navigated to friends list")
except Exception as e:
    print("❌ Could not find Friends tab:", e)
    driver.quit()
    exit()

time.sleep(10)

# === Scroll to load all friends ===
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("✅ All friends loaded")

# === Extract friends names and profile URLs ===
friends = driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com') and @role='link']")
friends_data = []

for f in friends:
    name = f.text.strip()
    url = f.get_attribute("href")
    if name and "profile.php" in url or "facebook.com/" in url:
        friends_data.append([name, url])

print(f"✅ Extracted {len(friends_data)} friends")

# === Save to CSV ===
with open("friends_list.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Profile URL"])
    writer.writerows(friends_data)

print("📁 Saved to friends_list.csv")

# Close browser
driver.quit()

