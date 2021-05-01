from agonesgr_scraper.spiders.agonesgr import AgonesgrSpider
import requests
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import os
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import dataset
import time
import schedule

DATABASE_URL = os.environ.get('DATABASE_URL')
db = dataset.connect(DATABASE_URL)
pred_table = db['predictions']

settings_file_path = 'agonesgr_scraper.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

settings = get_project_settings()
settings['FEEDS'] = {'games.json': {'format': 'json'}}
print(settings)
process = CrawlerProcess(settings)

def scrape_and_update():
	try:
		os.remove('games.json')
	except OSError:
		pass
		
	process.crawl(AgonesgrSpider, days_ago=100)
	process.start()

	df = pd.read_json('games.json')
	df['outcome'] = ['1' if home>away else '2' if away>home else 'X' for home,away in df['score']]
	clf = GaussianNB()
	clf.fit(df[['one', 'chi', 'two']], df['outcome'])

	games = []
	r = requests.get('https://agones.gr/ticker_minisite_show.php?navigation=yes')
	soup = BeautifulSoup(r.text, 'lxml')
	table = soup.find('table', {'class': 'ii__livescores'}).tbody
	rows = table.find_all('tr')
	for row in rows:
		cells = row.find_all('td')
		try:
			flag = cells[0].img.get('src')
			trnmnt = cells[0].img.get('title').strip()
			time = cells[1].text.strip()
			gid = int( cells[2].text )
			home, away = [x.strip() for x in cells[3].text.split('-')]
			one = float( cells[4].text )
			chi = float( cells[5].text )
			two = float( cells[6].text )
			game = {
				'flag': flag,
				'trnmnt': trnmnt,
				'time': time,
				'gid': gid,
				'home': home,
				'away': away,
				'one': one,
				'chi': chi,
				'two': two
			}
			games.append(game)
		except:
			pass

	pred_df = pd.DataFrame(games)
	pred_df['prediction'] = clf.predict(pred_df[['one', 'chi', 'two']])

	predictions = pred_df.to_dict('records')
	pred_table.drop()
	pred_table.insert_many(predictions)
	print('Updated database.\n')

scrape_and_update()
schedule.every(10).hours.do(scrape_and_update)

while True:
	schedule.run_pending()
	time.sleep(1)