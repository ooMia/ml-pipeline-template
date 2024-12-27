def main():
    from scrape import SCRAP_BASE_URL
    from scrape.DetailScraper import DetailScraper
    from scrape.Crawler import Crawler
    crawler = Crawler()
    page_max = 1
    base_url = SCRAP_BASE_URL
    from selenium import webdriver
    from scrape import driver_options
    driver = webdriver.Chrome(options=driver_options)
    for page in range(1, page_max + 1):
        for company in crawler.company_list_at(page):
            detail_scraper = DetailScraper(base_url + company['href'], driver)
            print(detail_scraper.keywords)
            print(detail_scraper.investment)
            print(detail_scraper.recruit)


if __name__ == '__main__':
    main()
