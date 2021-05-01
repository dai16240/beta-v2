import scrapy
import datetime as dt
from ..items import AgonesgrScraperItem


class AgonesgrSpider(scrapy.Spider):
	name = 'agonesgr'

	def __init__(self, days_ago=10, *args, **kwargs):
		super(AgonesgrSpider, self).__init__(*args, **kwargs)
		self.days_ago = int(days_ago)

		datetimes = [
			(dt.datetime.today()-dt.timedelta(days=0)) - dt.timedelta(days=i)
			for i in range(self.days_ago)
		]

		self.start_urls = [
			f'https://agones.gr/ticker_minisite_show.php?navigation=yes&date={d.year}-{str(d.month).zfill(2)}-{str(d.day).zfill(2)}'
			for d in datetimes
		]


	def parse(self, response):
		items = AgonesgrScraperItem()

		table = response.css('.ii__livescores tbody')
		rows = table.css('tr')
		for row in rows:
			cells = row.css('td')
			try:
				flag = cells[0].css('img::attr(src)').get()
				time = cells[1].css('td').css('::text').get()
				gid = int( cells[2].css('td').css('::text').get() )
				home, _dash, away = cells[3].css('td').css('::text').extract()
				one = float( cells[4].css('td').css('::text').get() )
				chi = float( cells[5].css('td').css('::text').get() )
				two = float( cells[6].css('td').css('::text').get() )
				score = [int(x) for x in cells[8].css('td').css('::text').get().split('-')]

				items['flag'] = flag
				items['time'] = time
				items['gid'] = gid
				items['home'] = home
				items['away'] = away
				items['one'] = one
				items['chi'] = chi
				items['two'] = two
				items['score'] = score

				yield items
			except:
				pass