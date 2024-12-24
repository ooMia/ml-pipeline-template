class DetailScraper:
    from scrap import SCRAP_DETAIL_SAMPLE_URL

    def __init__(self, url: str = SCRAP_DETAIL_SAMPLE_URL):
        from selenium import webdriver
        from selenium.webdriver.support.wait import WebDriverWait
        from scrap import driver_options

        self.driver = webdriver.Chrome(options=driver_options)
        self.wait = WebDriverWait(self.driver, 3)

        if not self.__is_login():
            self.__login()
        self.driver.get(url)
        self.__scrap_corp_keywords()
        self.__scrap_corp_investment()
        self.__scrap_corp_recruit()

    def __find_element_by(self, method: str, at: str):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions
        by = getattr(By, method)
        return self.wait.until(expected_conditions.presence_of_element_located((by, at)))

    def __find_element_by_selector(self, selector: str):
        from selenium.common import TimeoutException
        try:
            element = self.__find_element_by('CSS_SELECTOR', selector)
            self.driver.execute_script(f"document.querySelector('{selector}').scrollIntoView();")
            return element
        except TimeoutException:
            return None

    def __is_login(self):
        from selenium.common import JavascriptException
        try:
            return self.driver.execute_script("return window.localStorage.getItem('accessToken')") is not None
        except JavascriptException:
            return False

    def __login(self):
        from scrap import SCRAP_LOGIN_URL, SCRAP_LOGIN_USER_ID, SCRAP_LOGIN_USER_PW
        from selenium.common import TimeoutException

        self.driver.get(SCRAP_LOGIN_URL)
        self.__find_element_by('NAME', 'email').send_keys(SCRAP_LOGIN_USER_ID)
        self.__find_element_by('NAME', 'password').send_keys(SCRAP_LOGIN_USER_PW)

        try:
            self.__find_element_by('CSS_SELECTOR', 'main form').submit()
        except TimeoutException:
            import pyautogui
            pyautogui.moveTo(600, 797)  # print(pyautogui.position())
            pyautogui.click()

        self.wait.until(lambda check: self.__is_login())

    def __scrap_corp_keywords(self):
        from scrap import SCRAP_DETAIL_CORP_FIELD_XPATH
        element = self.__find_element_by('XPATH', SCRAP_DETAIL_CORP_FIELD_XPATH)
        self.keywords = element.text.split('\n')[::2]

    def __scrap_corp_investment(self):
        from scrap import SCRAP_DETAIL_INVESTMENT_SELECTOR
        raw_text = self.__find_element_by_selector(SCRAP_DETAIL_INVESTMENT_SELECTOR).text

        import re
        self.investment = {
            "update": re.search(r"업데이트 : (.+)", raw_text).group(1),
            "stage": re.search(r"최종투자단계\n(.+)", raw_text).group(1),
            "amount": re.search(r"누적투자유치금액\n(.+)", raw_text).group(1),
            "count": re.search(r"투자유치건수\n(.+)", raw_text).group(1),
        }

    def __scrap_corp_recruit(self):
        e = self.__find_element_by_selector("#section-recruit")
        self.recruit = e.text if e is not None else None


if __name__ == '__main__':
    detail_scraper = DetailScraper()
    print(detail_scraper.keywords)
    print(detail_scraper.investment)
    print(detail_scraper.recruit)
