import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        #using xpath method
      #  title=response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a").getall()
        for country in countries:
            name = country.xpath(".//text()")
            link = country.xpath(".//@href()")
            yield{
                'country_name':name,
                'country_link':link
            }
        
