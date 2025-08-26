import scrapy
import logging

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
        #using xpath method
        countries = response.xpath("//td/a")
        for country in countries:
            name=country.xpath(".//text()").get()
            link=country.xpath(".//@href").get()

           # absolute_url = f"https://www.worldometers.info/{link}"
           # absolute_url = response.urljoin(link)
           # yield scrapy.Request(url=absolute_url)
            yield response.follow(url=link, headers=self.custom_headers,callback=self.parse_country)
        
    def parse_country(self,response):
        rows = response.xpath("(//table[contains(@class,'datatable')])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/text()").get()
        yield {
            'year' : year,
            'population' : population
        }   