import scrapy
from .. import IndeedItem


class IndeedSpider(scrapy.Spider):
	name = "indeed"
	page_num = 1
	def start_requests(self):
		enter_search = 'Python Developers'
		urls = [
			'https://www.indeed.co.in/jobs?q={}'.format(enter_search.lower().replace(' ','+'))
			]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
	def parse(self, response):
		items = IndeedItem()
		all_jobs_page = response.xpath("//div[contains(@class, 'jobsearch-SerpJobCard') and contains(@class, 'unifiedRow')]")
		titles = all_jobs_page[0].xpath('//div[@class = "title"]/a/@title').extract()
		companies = all_jobs_page[0].xpath('//div[@class = "sjcl"]/div/span//text()').extract() # Can be processed later
		items['job_title'] = titles
		items['company'] = companies
		yield items
		next_page = "https://www.indeed.co.in/jobs?q=python+developer&start={}".format(IndeedSpider.page_num*10)
		if IndeedSpider.page_num < 10:
			IndeedSpider.page_num += 1
			yield response.follow(next_page, callback = self.parse)


