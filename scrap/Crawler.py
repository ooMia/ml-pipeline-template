class Crawler:
    from selenium.webdriver.remote.webelement import WebElement

    def __init__(self):
        from selenium import webdriver
        from selenium.webdriver.support.wait import WebDriverWait
        from scrap import driver_options

        self.base_url = "https://www.innoforest.co.kr/dataroom?orderByField=invstWholeVal&page="
        self.page = 1
        self.driver = webdriver.Chrome(options=driver_options)
        self.wait = WebDriverWait(self.driver, 3)

    def __find_element_by(self, method: str, at: str) -> WebElement:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions
        by = getattr(By, method)
        return self.wait.until(expected_conditions.presence_of_element_located((by, at)))

    def company_list_at(self, page_number: int = 1):
        def __parse_html(raw_html):
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(raw_html, 'html.parser')
            tr_tags = soup.find_all('tr')

            result = []
            for tr in tr_tags:
                tr_dict = {
                    "href": tr.find('a')['href'],
                    "corp": tr.find(class_='corp').text,
                    "prod": tr.find(class_='prod').text,
                }
                result.append(tr_dict)
            return result

        self.driver.get(self.base_url + str(page_number))
        e = self.__find_element_by('TAG_NAME', 'tbody')
        return __parse_html(e.get_attribute('outerHTML')) if e is not None else None


if __name__ == '__main__':
    for c in Crawler().company_list_at(1):
        print(c)
