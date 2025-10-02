
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# === Your Facebook credentials ===
FB_EMAIL = "your_email_here"
FB_PASSWORD = "your_pass_here"

# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.facebook.com/")

time.sleep(20)

# Login
email_box = driver.find_element(By.ID, "email")
password_box = driver.find_element(By.ID, "pass")
email_box.send_keys(FB_EMAIL)
password_box.send_keys(FB_PASSWORD)
password_box.send_keys(Keys.RETURN)

print("Login submitted...")
time.sleep(30)

# Check login
if "facebook.com" not in driver.current_url:
    print("❌ Login failed.")
    driver.quit()
    exit()

print("✅ Logged in successfully!")

# Go to home feed
driver.get("https://www.facebook.com/")
time.sleep(5)

# Scroll and collect posts
SCROLL_PAUSE_TIME = 2
posts_data = []
scroll_count = 5  # number of scrolls

last_height = driver.execute_script("return document.body.scrollHeight")

for scroll in range(scroll_count):
    print(f"Scrolling {scroll+1}/{scroll_count}...")
    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

    posts = driver.find_elements(By.XPATH, '//div[contains(@role,"article")]')

    for post in posts:
        try:
            post_text = post.text.strip()
            if post_text not in posts_data:
                posts_data.append(post_text)
        except:
            continue

    # Check if page height changed
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print(f"\nCollected {len(posts_data)} posts.\n")

# Display scraped posts
for i, post_content in enumerate(posts_data[:20]):  # show first 20 posts
    print(f"Post {i+1}:\n{post_content}\n{'-'*50}")

driver.quit()

