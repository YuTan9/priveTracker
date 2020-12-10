import requests
from bs4 import BeautifulSoup
import webbrowser
from datetime import date, datetime
import os
import csv
from matplotlib import pyplot as plt
import sys

def render():
	time = []
	discounts = []
	os.chdir("..")
	with open('log.csv', 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			time.append(row[0])
			discounts.append(int(row[1]))
	plt.xlabel("Date")
	plt.ylabel("__%% off")
	plt.plot(time, discounts, 'r.-')
	plt.title('discounts')
	plt.savefig('discount.png')
		

def crawl():
	today = date.today()
	# dd/mm/YY
	d1 = today.strftime("%Y%m%d")

	URL = 'https://www.myprotein.tw/voucher-codes.list'
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

	page = requests.get(URL, headers = headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	soup.encoding = 'utf-8'
	title = soup.findAll("h2", {"class": "voucher-title"})
	day   = soup.findAll("div", {"class": "voucher-end-date"})
	msg   = soup.findAll("div", {"class": "voucher-message"})
	numbers = [d.string for d in title]

	print(str('crawled objects\' sizes: ') + str((len(title), len(day), len(msg))))
	if len(title) != len(day) or len(title) != len(msg) or len(day) != len(msg):
		return 1
	discounts = []
	for t in title:
		tmp = t.text.split(u' ')
		for i in range(len(tmp)):
			if tmp[i] == u'\u6298':
				if int(tmp[i-1]) < 10:
					discounts.append(100-int(tmp[i-1])*10)
				else:
					discounts.append(100-int(tmp[i-1]))

	fields=[today, max(discounts)]
	with open('log.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerow(fields)

	os.chdir("events")
	filename = "event" + d1 + ".html"
	with open(filename,"w+") as f:
		for i in range(len(numbers)):
			f.write(title[i].prettify("UTF-8", formatter="html").replace("class=\"voucher-title\"", "class=\"voucher-title\" style=\"font-size:40pt; color: red\""))
			f.write(day [i].prettify("UTF-8", formatter="html").replace("class=\"voucher-end-date no-timer\"", "class=\"voucher-end-date no-timer\" style=\"font-size:9pt\""))
			f.write(msg[i].prettify("UTF-8", formatter="html").replace("strong", "p style=\"font-size:12pt\""))
			f.write("<br><br><br><br>")

	cwd = os.getcwd()
	# webbrowser.open("file://" + cwd + "/" + filename, new = 2)
	return 0

def main():
	if crawl() != 0:
		sys.exit("Something went wrong.")
	else:
		print('Start render()...')
		render()

if __name__ == "__main__":
	main()
