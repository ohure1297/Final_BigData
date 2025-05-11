import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, time

# Khởi tạo undetected Chrome
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)
driver = uc.Chrome(options=options)

jobs = []
max_pages = 20
base_url = "https://www.vietnamworks.com/viec-lam?q=cong-nghe-thong-tin"

def scroll_window_to_end(driver, pause=1.5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)

try:
    for p in range(1, max_pages + 1):
        url = f"{base_url}&page={p}"
        driver.get(url)
        print(f"Loading page {p}: {url}")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.search_list.view_job_item"))
        )

        prev_count = 0
        while True:
            cards = driver.find_elements(By.CSS_SELECTOR, "div.search_list.view_job_item")
            curr_count = len(cards)
            if curr_count == prev_count:
                break
            prev_count = curr_count
            scroll_window_to_end(driver)

        print(f"Page {p}: total {curr_count} jobs loaded")
        if curr_count == 0:
            break

        # Thu thập thông tin
        for card in cards:
            try:
                a_tag = card.find_element(By.CSS_SELECTOR, "h2 a")
                try:
                    span = a_tag.find_element(By.TAG_NAME, "span")
                    driver.execute_script("arguments[0].remove();", span)
                except:
                    pass
                title = a_tag.text.strip()
            except:
                title = None
            
            try:
                company = card.find_element(By.CSS_SELECTOR, "div.sc-cdaca-d a").text.strip()
            except:
                company = None
            
            salary, address = None, None
            try:
                spans = card.find_elements(By.CSS_SELECTOR, "div.sc-bwGlVi.guifwN span")
                if spans:
                    salary = spans[0].text.strip()
                if len(spans) > 1:
                    address = spans[1].text.strip()
            except:
                pass

            jobs.append({
                "title": title,
                "company": company,
                "address": address,
                "salary": salary
            })

finally:
    try:
        driver.quit()
    except:
        pass

# Lưu kết quả
with open("vnwork.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)

print(f"Saved {len(jobs)} jobs to vnwork.json")
