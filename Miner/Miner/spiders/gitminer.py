import scrapy

class GitMiner(scrapy.Spider):
    name = 'gitminer'
    # start_urls = ['https://github.com/iluwatar/java-design-patterns']

    # def parse(self, response):
    #     for title in response.css('.post-header>h2'):
    #         yield {'title': title.css('a ::text').get()}

    #     for next_page in response.css('div.prev-post > a'):
    #         yield response.follow(next_page, self.parse)

    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall(),
    #         }

    def start_requests(self):
        # urls = ['https://github.com/iluwatar/java-design-patterns']
        urls = [
            'https://github.com/iluwatar/java-design-patterns',
            'https://github.com/iluwatar/java-design-patterns/blob/master/abstract-document/src/main/java/com/iluwatar/abstractdocument/AbstractDocument.java',
            'https://raw.githubusercontent.com/iluwatar/java-design-patterns/master/abstract-document/src/main/java/com/iluwatar/abstractdocument/AbstractDocument.java',
            'https://raw.githubusercontent.com/iluwatar/java-design-patterns/master/abstract-document/src/main/java/com/iluwatar/abstractdocument/App.java',
        ]
        ## Need to extract raw contant and fix referencing
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = '%s' % page
        # filename = 'gitfile.html'
        content = response.xpath('//*[@id="d3c24aa2b96948b1966b4ffac26a26c9-299b431996612168d2bc289ec3879729293e6ae6"]').extract()
        # TODO: Need to optimize for different folder structures
        print('\nContent ---- ',content)

        next_url = response.css('.js-navigation-open a ::attr("href")').extract()
        print('\nURL ---- ',next_url)

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)