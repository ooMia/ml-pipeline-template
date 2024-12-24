from scrap.scrap_detail import DetailScraper


def test_login():
    scraper = DetailScraper()
    assert scraper._is_login() is False
    scraper._login()
    assert scraper._is_login() is True
