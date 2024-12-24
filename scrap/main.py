from urllib import parse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrap import SCRAP_INITIAL_URL

options = Options()
driver = webdriver.Chrome(options=options)
driver.get(SCRAP_INITIAL_URL)

html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())

# 모든 a 태그 찾기
a_tags = soup.find_all('a')

for tag in a_tags:
    href = tag.get('href')
    if href and href.startswith('/company'):
        encoded_part = href.split('/')[-1]
        decoded_part = parse.unquote(encoded_part)
        print(f"내용: {tag.text}, URL: {href}, 디코딩된 부분: {decoded_part}")
