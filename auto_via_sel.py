from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument("--headless") # Runs Chrome in the background
options.add_argument("--disable-gpu")


driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get("https://thehackernews.com/")
print("woring properly")
conatiner =driver.find_elements("xpath",'//div[@class="clear home-right"]')

#//div[@class="clear home-right"] 
Title=[]
Subtitle=[]
Link=[]
news_dict={}

for i in conatiner:
    title = i.find_element("xpath",'./h2').text 
    subtitle = i.find_element("xpath",'./div[@class ="home-desc"]').text
    link = driver.find_element("xpath",'//div[@class="body-post clear"]/a').get_attribute("href")
    print("Title: ",title)
    print("Subtitle: ",subtitle)    
    print("Link: ",link)
    print("##########################################################")
    Title.append(title)
    Subtitle.append(subtitle)
    Link.append(link)

news_dict={"title":Title,"subtitle":Subtitle,"Link":Link}

df=pd.DataFrame(news_dict)
df.to_csv("news.csv",index=False)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_message = f"[SUCCESS] news.csv updated at: {current_time}\n"

with open("scraper.log", "a") as log_file:
    log_file.write(log_message)

print(log_message.strip())







driver.quit()
