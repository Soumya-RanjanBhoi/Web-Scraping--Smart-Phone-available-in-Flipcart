from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import regex as re
from selenium.common.exceptions import TimeoutException


base_url="https://www.flipkart.com/search?q=smartphones&page={}"

class SmartPhone(webdriver.Chrome):
    def __init__(self, driver_path="D:/selenium/chromedriver-win64/chromedriver.exe"):
        self.path = driver_path
        service = Service(self.path)
        super().__init__(service=service)

    def data_collect(self, total_pages=1):
        all_img_urls = []
        all_phones_data = []
        all_ratings = []
        all_mobiles = []
        cost_without_dis = []
        cost_with_dis = []

        wait = WebDriverWait(self, 15)

        for page in range(1, total_pages + 1):
            print(f"\nScraping Page {page}")
            self.get(base_url.format(page))

            try:
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tUxRFH')))
                time.sleep(2)
            except TimeoutException:
                print("⏳ Timeout: Products didn't load.")
                continue

            soup = BeautifulSoup(self.page_source, 'html.parser')
            container = soup.find_all('div', class_='tUxRFH')

            for datas in container:
                img_tag = datas.find_all('img', class_='DByuf4')
                text = str(img_tag)
                match = re.search(r'src="([^"]+)"', text)
                all_img_urls.append(match.group(1) if match else "No Image")

                about = datas.find_all('div', class_='KzDlHZ')
                all_phones_data.append(about[0].text.strip() if about else "No Name")

                rate = datas.find_all('div', class_='XQDdHH')
                all_ratings.append(rate[0].text.strip() if rate else "No Rating")

                temp = datas.find_all('li', class_='J+igdf')
                items = [li.text.strip() for li in temp]
                current_mobile = []
                has_warranty = False

                for item in items:
                    current_mobile.append(item)
                    if "warranty" in item.lower():
                        has_warranty = True
                        break

                if not has_warranty:
                    current_mobile.append("No Warranty")

                all_mobiles.append(current_mobile)

                cost_wo = datas.find_all('div', class_='Nx9bqj _4b5DiR')
                cost_without_dis.append(cost_wo[0].text if cost_wo else "N/A")

                cost_w = datas.find_all('div', class_='yRaY8j ZYYwLA')
                cost_with_dis.append(cost_w[0].text if cost_w else "N/A")

        print("\nScraping Finished")

        return {
            "image_urls": all_img_urls,
            "titles": all_phones_data,
            "ratings": all_ratings,
            "specs": all_mobiles,
            "price_without_discount": cost_without_dis,
            "price_with_discount": cost_with_dis
        }

