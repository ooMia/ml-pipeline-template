class DetailScraper:
    from scrap import SCRAP_DETAIL_SAMPLE_URL

    def __init__(self, url: str = SCRAP_DETAIL_SAMPLE_URL):
        from selenium import webdriver
        from selenium.webdriver.support.wait import WebDriverWait
        from scrap import driver_options

        self.url = url
        self.driver = webdriver.Chrome(options=driver_options)
        self.wait = WebDriverWait(self.driver, 10)

    def _find_element_by(self, method: str, at: str):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions
        by = getattr(By, method)
        return self.wait.until(expected_conditions.presence_of_element_located((by, at)))

    def _find_element_by_selector(self, selector: str):
        element = self._find_element_by('CSS_SELECTOR', selector)
        self.driver.execute_script(f"document.querySelector('{selector}').scrollIntoView();")
        return element

    def _is_login(self):
        from selenium.common import JavascriptException
        try:
            return self.driver.execute_script("return window.localStorage.getItem('accessToken')") is not None
        except JavascriptException:
            return False

    def _login(self):
        from scrap import SCRAP_LOGIN_URL, SCRAP_LOGIN_USER_ID, SCRAP_LOGIN_USER_PW
        self.driver.get(SCRAP_LOGIN_URL)
        self._find_element_by('NAME', 'email').send_keys(SCRAP_LOGIN_USER_ID)
        self._find_element_by('NAME', 'password').send_keys(SCRAP_LOGIN_USER_PW)

        import pyautogui
        pyautogui.moveTo(600, 797)  # print(pyautogui.position())
        pyautogui.click()

    def scrap_corp_keywords(self) -> list:
        from scrap import SCRAP_DETAIL_CORP_FIELD_XPATH

        self.driver.get(self.url)
        element = self._find_element_by('XPATH', SCRAP_DETAIL_CORP_FIELD_XPATH)
        return element.text.split('\n')[::2]

    def scrap_corp_investment(self) -> dict:
        if not self._is_login():
            self._login()

        self.driver.get(self.url)
        from scrap import SCRAP_DETAIL_INVESTMENT_SELECTOR
        raw_text = self._find_element_by_selector(SCRAP_DETAIL_INVESTMENT_SELECTOR).text

        import re
        return {
            "update": re.search(r"업데이트 : (.+)", raw_text).group(1),
            "stage": re.search(r"최종투자단계\n(.+)", raw_text).group(1),
            "amount": re.search(r"누적투자유치금액\n(.+)", raw_text).group(1),
            "count": re.search(r"투자유치건수\n(.+)", raw_text).group(1),
        }


if __name__ == '__main__':
    detail_scraper = DetailScraper()
    print(detail_scraper.scrap_corp_investment())
    print(detail_scraper.scrap_corp_keywords())
