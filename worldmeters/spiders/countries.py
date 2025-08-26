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
        title=response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a/text()").getall()

        yield{
            'title':title,
            'countries':countries
        }
        
