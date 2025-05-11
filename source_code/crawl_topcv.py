import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, time

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)
driver = uc.Chrome(options=options)

jobs = []
max_pages = 20

try:
    url = "https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257?category_family=r257"
    driver.get(url)

    for p in range(1, max_pages+1):
        container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-list-search-result"))
        )
        items = container.find_elements(By.CSS_SELECTOR, ":scope > div")
        print(f"Page {p}: found {len(items)} jobs")

        for job in items:
            jobs.append({
                "title":   job.find_element(By.CSS_SELECTOR, ".body-content h3 a span").text.strip(),
                "company": job.find_element(By.CLASS_NAME, "company").text.strip(),
                "address": job.find_element(By.CLASS_NAME, "address").text.strip(),
                "salary":  job.find_element(By.CLASS_NAME, "title-salary").text.strip()
            })

        try:
            nxt = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
            next_url = nxt.get_attribute("data-href") or nxt.get_attribute("href")
            if not next_url:
                break
            driver.get(next_url)
            time.sleep(5)   
        except:
            break

finally:
    driver.quit()

with open("topcv.json","w",encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)

print(f"Saved {len(jobs)} jobs to topcv.json")
