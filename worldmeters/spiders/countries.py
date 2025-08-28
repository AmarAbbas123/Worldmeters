import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']
    
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.custom_headers)

    def parse(self, response):
        countries = response.xpath("//table[contains(@class, 'datatable')]/tbody/tr")
        for country in countries:
            rank = country.xpath("./td[1]/text()").get()
            name = country.xpath("./td[2]/a/text()").get()
            link = country.xpath("./td[2]/a/@href").get()

            yield response.follow(
                url=link,
                headers=self.custom_headers,
                callback=self.parse_country,
                meta={'country': name, 'rank': rank}
            )

  
    def parse_country(self, response):
        country = response.meta['country']
        rank = response.meta['rank']
        rows = response.xpath("(//table[contains(@class,'datatable')])[2]/tbody/tr")

        for row in rows:
            yield {
                "rank":rank,
                'country': country,
                'year': row.xpath(".//td[1]/text()").get(),
                'population': row.xpath(".//td[2]/text()").get(),
                'Yearly_%_Change': row.xpath(".//td[3]/text()").get(),
                'Yearly_Change': row.xpath(".//td[4]/text()").get(),
                "Migrants_(net)": row.xpath(".//td[5]/text()").get(),
                "Median Age": row.xpath(".//td[6]/text()").get(),
                "Fertility Rate": row.xpath(".//td[7]/text()").get(),
                "Density (P/Km²)": row.xpath(".//td[8]/text()").get(),
                "Urban_Pop %": row.xpath(".//td[9]/text()").get(),
                "Urban Population": row.xpath(".//td[10]/text()").get(),
                "Country's Share of World Pop": row.xpath(".//td[11]/text()").get(),
                "World_Population": row.xpath(".//td[12]/text()").get(),
                "Global Rank": row.xpath(".//td[13]/text()").get()
            }
