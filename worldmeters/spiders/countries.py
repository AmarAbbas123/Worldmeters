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
            yield response.follow(
                url=link,
                headers=self.custom_headers,
                callback=self.parse_country,
                meta={'country': name}
            )

        
    def parse_country(self,response):
        country = response.meta['country']
        rows = response.xpath("(//table[contains(@class,'datatable')])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/text()").get()
            Yearly_percent_Change = row.xpath(".//td[3]/text()").get()
            Yearly_Change = row.xpath(".//td[4]/text()").get()
            Migrants = row.xpath(".//td[5]/text()").get()
            Median = row.xpath(".//td[6]/text()").get()
            Fertility = row.xpath(".//td[7]/text()").get()
            Density = row.xpath(".//td[8]/text()").get()
            Urban_Pop  = row.xpath(".//td[9]/text()").get()
            Urban_Population = row.xpath(".//td[10]/text()").get()
            Country_Share = row.xpath(".//td[11]/text()").get()
            World_Population = row.xpath(".//td[12]/text()").get()
            Pakistan_Global_Rank = row.xpath(".//td[13]/text()").get()

        yield {
            'country': country,
            'year' : year,
            'population' : population,
            'Yearly_%_Change': Yearly_percent_Change,
            'Yearly_Change'  : Yearly_Change,
            "Migrants_(net)" : Migrants,
            "Median Age" : Median,
            "Fertility Rate" :Fertility,
            "Density (P/Km²)" : Density,
            "Urban_Pop %": Urban_Pop,
            "Urban Population" : Urban_Population,
            "Country's Share of World Pop" : Country_Share,
            "World_Population" : World_Population,
            "Pakistan Global Rank" : Pakistan_Global_Rank

        }   