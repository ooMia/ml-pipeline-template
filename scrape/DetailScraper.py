class DetailScraper:
    from selenium.webdriver.remote.webelement import WebElement
    from scrape import SCRAPE_DETAIL_SAMPLE_URL

    def __init__(self, url: str = SCRAPE_DETAIL_SAMPLE_URL, driver=None):
        from selenium import webdriver
        from selenium.webdriver.support.wait import WebDriverWait
        from scrape import driver_options

        self.__driver = driver
        if driver is None:
            self.__driver = webdriver.Chrome(options=driver_options)
        self.__wait = WebDriverWait(self.__driver, 3)

        if not self.__is_login():
            self.__login()
        self.__driver.get(url)
        self.__scrap_corp_keywords()
        self.__scrap_corp_investment()
        self.__scrap_corp_recruit()

    def __find_element_by(self, method: str, at: str) -> WebElement:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions
        by = getattr(By, method)
        return self.__wait.until(expected_conditions.presence_of_element_located((by, at)))

    def __find_element_by_selector(self, selector: str) -> WebElement or None:
        from selenium.common import TimeoutException
        try:
            element = self.__find_element_by('CSS_SELECTOR', selector)
            self.__driver.execute_script(f"document.querySelector('{selector}').scrollIntoView();")
            return element
        except TimeoutException:
            return None

    def __is_login(self):
        from selenium.common import JavascriptException
        try:
            return self.__driver.execute_script("return window.localStorage.getItem('accessToken')") is not None
        except JavascriptException:
            return False

    def __login(self):
        from scrape import SCRAPE_LOGIN_URL, SCRAPE_LOGIN_USER_ID, SCRAPE_LOGIN_USER_PW
        from selenium.common import TimeoutException

        self.__driver.get(SCRAPE_LOGIN_URL)
        self.__find_element_by('NAME', 'email').send_keys(SCRAPE_LOGIN_USER_ID)
        self.__find_element_by('NAME', 'password').send_keys(SCRAPE_LOGIN_USER_PW)

        try:
            self.__find_element_by('CSS_SELECTOR', 'main form').submit()
        except TimeoutException:
            import pyautogui
            pyautogui.moveTo(600, 797)  # print(pyautogui.position())
            pyautogui.click()

        self.__wait.until(lambda check: self.__is_login())

    def __scrap_corp_keywords(self):
        from scrape import SCRAPE_DETAIL_CORP_FIELD_XPATH
        element = self.__find_element_by('XPATH', SCRAPE_DETAIL_CORP_FIELD_XPATH)
        self.keywords = element.text.split('\n')[::2]

    def __scrap_corp_investment(self):
        from scrape import SCRAPE_DETAIL_INVESTMENT_SELECTOR
        raw_text = self.__find_element_by_selector(SCRAPE_DETAIL_INVESTMENT_SELECTOR).text

        import re
        self.investment = {
            "update": re.search(r"업데이트 : (.+)", raw_text).group(1),
            "stage": re.search(r"최종투자단계\n(.+)", raw_text).group(1),
            "amount": re.search(r"누적투자유치금액\n(.+)", raw_text).group(1),
            "count": re.search(r"투자유치건수\n(.+)", raw_text).group(1),
        }

    def __scrap_corp_recruit(self):
        def __click_load_button():
            while True:
                button = self.__find_element_by_selector("#section-recruit > div > div > div > div > div > button")
                if button is None:
                    break
                self.__driver.execute_script("arguments[0].click();", button)

        def __parse_html(raw_html):
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(raw_html, 'html.parser')
            li_tags = soup.find_all('li')

            result = []
            for li in li_tags:
                li_dict = {
                    "href": li.find('a')['href'],
                    "name": li.find('h1').text,
                    "incentive": li.find('p').text,
                    "type": li.find('span').text
                }
                result.append(li_dict)
            return result

        __click_load_button()
        e = self.__find_element_by_selector("#section-recruit")
        self.recruit = __parse_html(e.get_attribute('outerHTML')) if e is not None else None


if __name__ == '__main__':
    detail_scraper = DetailScraper()
    print(detail_scraper.keywords)
    print(detail_scraper.investment)
    print(detail_scraper.recruit)
    print(len(detail_scraper.recruit))
