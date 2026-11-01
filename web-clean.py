from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
import time
from llm import get_urls
from bs4 import BeautifulSoup
import feedparser
from urllib.parse import urljoin



Service = Service(ChromeDriverManager().install())

webdriver=webdriver.Chrome(service=Service)

urls=get_urls().splitlines()  # Split the string into a list of URLs
# urls = ['https://www.techmeme.com', 'https://www.geekwire.com', 'https://www.cloudcomputing-news.net', 'https://www.infoq.com', 'https://www.zdnet.com', 'https://www.crn.com', 'https://www.itpro.co.uk', 'https://www.computerweekly.com', 'https://www.infoworld.com', 'https://www.computing.co.uk']
# test_urls = ['https://thehackernews.com/', 'https://www.techmeme.com']
# for url in urls:
#     webdriver.get(url)
#     time.sleep(5)  # Wait for the page to load
# print(urls)
rss_feeds = []
for url in urls:
    webdriver.get(url)
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "")
    file_name = f"web_content_{safe_name}.txt"
    html_content = webdriver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    # unwanted_tags = [
    #     'script', 'style', 'noscript', 'nav', 'header', 'footer', 
    #     'aside', 'form', 'button', 'iframe', 'svg',
    # ]

    # for tag in soup.find_all(unwanted_tags):
    #     tag.decompose()

    # head = soup.find('head')
    # for links in head.find_all('link'):
    #     type_attr = links.get("type")
    #     print(type_attr)

    head = soup.find('head')
    for links in head.find_all('link'):
         type_attr = links.get("type")

         
         if type_attr=="application/rss+xml" or type_attr=="application/atom+xml":
            rss_link = links.get("href")
            print(f"RSS feed found: {rss_link}")
            if rss_link.startswith("http://") or rss_link.startswith("https://"):
                rss_feeds.append(rss_link)
            else:
                base_website_url = url
                full_link = urljoin(base_website_url, rss_link)
                rss_feeds.append(full_link)
                
         

    with open(file_name,'w',encoding="utf-8") as f:
        f.write(soup.prettify())

    
for rss in rss_feeds:
    print(f"RSS feed found: {rss}")








def fetch_rss_feed(rss_url):

    
    
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        print(f"Failed to fetch or empty RSS feed from {rss_url}.")
        return

    # GATEKEEPER: Isolate the first item in the list
    first_item = feed.entries[0]
    
    # Check if the required fields exist on that first item
    if not first_item.get('title') or not first_item.get('link') or not first_item.get('summary'):
        print(f"RSS feed from {rss_url} is missing required text fields. Skipping.")
        return
        
    # Check for media enclosures to filter out podcasts/videos
    if first_item.get('enclosures'):
        print(f"Podcast or media feed detected at {rss_url}. Skipping.")
        return

    # If the feed passes the gatekeeper, process the entries
    for i in feed.entries[:1]:
        print(f"Title: {i.get('title')}")
        print(f"Link: {i.get('link')}")
        
        print("\n")
        
    print(f"Fetched {len(feed.entries[:2])} entries from {rss_url}\n")


for rss in rss_feeds:
    fetch_rss_feed(rss)
        
    






