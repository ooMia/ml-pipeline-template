def main():
    from scrape import SCRAPE_CUR_PAGE, SCRAPE_BASE_URL, driver_options
    from scrape.DetailScraper import DetailScraper
    from scrape.Crawler import Crawler
    from scrape.model import Company
    from db.CompanyDB import CompanyDB
    from selenium.webdriver import Firefox

    cur_page = SCRAPE_CUR_PAGE
    driver = Firefox(options=driver_options, )
    for page in range(cur_page, cur_page + 1):
        for company in Crawler(driver).company_list_at(page):
            url = SCRAPE_BASE_URL + company['href']
            print(url)
            ds = DetailScraper(url, driver)
            c = Company.get_instance_by_href(url, ds)
            CompanyDB().store_company(c)

    import os
    from dotenv import set_key
    set_key(
        os.path.join(os.path.dirname(__file__), '.env'),
        'SCRAPE_CUR_PAGE',
        str((cur_page % 10) + 1))


if __name__ == '__main__':
    main()
