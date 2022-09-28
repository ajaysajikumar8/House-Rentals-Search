import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


CHROMEDRIVER_PATH = "D:\chromedriver_win32\chromedriver.exe"
zillow_url = r"https://www.zillow.com/los-angeles-ca/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A34.36808533201717%2C%22east%22%3A-117.87202913085937%2C%22south%22%3A33.67263073413185%2C%22west%22%3A-118.95143586914062%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12447%2C%22regionType%22%3A6%7D%5D%7D"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language" : "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6"
}

#------------------------SCRAPING THE DATA USING BEAUTIFUL SOUP-------------------
response = requests.get(url=zillow_url, headers=headers)
website_data = response.text

soup = BeautifulSoup(website_data,"html.parser")

all_address = []
address_elements = soup.find_all(name="address", attrs={"data-test": "property-card-addr"})
for address_element in address_elements:
    address = address_element.get_text()
    all_address.append(address)

all_links = []
link_elements = soup.findAll(name="a", attrs= {"data-test" : "property-card-link","tabindex":"0"})
for link_element in link_elements:
    link = link_element["href"]
    all_links.append(link)
        
all_prices = []
price_element = soup.find_all(name="span", attrs={"data-test" :"property-card-price"}, limit=None)
for element in price_element:
    price = element.get_text()
    all_prices.append(price)


#---------------------------USING SELENIUM TO AUTOMATE FILLINF OF GOOGLE FORMS-------------------
bot = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
bot.get("https://forms.gle/Z5b13am6gTx7DdMA8")

time.sleep(5)

for x in range(len(all_address) - 1):
    address_label = bot.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    price_label = bot.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    link_label = bot.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    submit_btn = bot.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    time.sleep(2)
    address_label.send_keys(all_address[x])
    time.sleep(1)
    price_label.send_keys(all_prices[x])
    time.sleep(1)
    link_label.send_keys(all_links[x])
    time.sleep(1)
    submit_btn.click()
    time.sleep(2)
    submit_another = bot.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another.click()
    time.sleep(5)