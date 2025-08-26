import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/115.0 Safari/537.36"
                }
            )

    def parse(self, response):
        #using xpath method
        countries = response.xpath("//td/a")
        for country in countries:
            name=country.xpath(".//text()").get()
            link=country.xpath(".//@href").get()
            yield{
                'title' : name,
                'countries_link': link
            }
        
