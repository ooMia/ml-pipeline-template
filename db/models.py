from dataclasses import dataclass

from scrape.DetailScraper import DetailScraper


@dataclass
class CompanyInvestment:
    update: str
    stage: str
    amount: str
    count: str

    def __init__(self, ds: DetailScraper):
        self.update = ds.investment['update']
        self.stage = ds.investment['stage']
        self.amount = ds.investment['amount']
        self.count = ds.investment['count']


@dataclass
class CompanyRecruitDetail:
    href: str
    name: str
    incentive: str
    type: str


@dataclass
class CompanyRecruit:
    detail: list[CompanyRecruitDetail]

    def __init__(self, ds: DetailScraper):
        self.detail = [CompanyRecruitDetail(**d) for d in ds.recruit]


@dataclass
class Company:
    id: str
    name: str
    keyword: list[str]
    investment: CompanyInvestment
    recruit: CompanyRecruit

    def __init__(self, href):
        import urllib.parse
        self.id = href.split('/')[-2]
        self.name = urllib.parse.unquote(href.split('/')[-1])

        from scrape.DetailScraper import DetailScraper
        ds = DetailScraper(href)
        self.keyword = ds.keywords
        self.investment = CompanyInvestment(ds)
        self.recruit = CompanyRecruit(ds)

    def href(self):
        import urllib.parse
        return str.join(self.id, urllib.parse.quote(self.name))


if __name__ == '__main__':
    from pprint import pprint
    from scrape import SCRAP_DETAIL_SAMPLE_URL

    company = Company(SCRAP_DETAIL_SAMPLE_URL)
    pprint(company)
