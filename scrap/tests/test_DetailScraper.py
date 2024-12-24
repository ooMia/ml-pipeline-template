from scrap.scrap_detail import DetailScraper

scraper = DetailScraper()


def test_investment():
    assert scraper.investment.get('update') is not None
    assert scraper.investment.get('stage') is not None
    assert scraper.investment.get('amount') is not None
    assert scraper.investment.get('count') is not None


def test_keywords():
    assert len(scraper.keywords) > 0


def test_hiring():
    assert scraper.recruit is not None
