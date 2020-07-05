import time
import io

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen as uReq #parse url text
from bs4 import BeautifulSoup as soup #grab page

myurl = 'https://steamcommunity.com/app/275850/reviews/?browsefilter=toprated&snr=1_5_100010_'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(myurl)
time.sleep(1)

elem = driver.find_element_by_tag_name("html")

no_of_pagedowns = 5000 #how many number of pagedowns you want to do

#this will open a chrome window that will automatically press the no_of_pagedowns 
while no_of_pagedowns:
	elem.send_keys(Keys.PAGE_DOWN)
	time.sleep(0.2)
	no_of_pagedowns -= 1

#parse html
page_soup = soup(driver.page_source, "html.parser")

#grab reviews
review = page_soup.findAll("div",{"class":"apphub_Card modalContentLink interactable"})

#make the csv file
filename = "reviews.csv"
f = io.open(filename, "w", encoding="utf-8")

#headers of csv file
headers = "recommend, date, review\n"

f.write(headers)

#write the review data into the csv file
for rev in review:
	recc_Container = rev.findAll("div",{"class":"title"})
	recommended = recc_Container[0].text

	date_Container = rev.findAll("div",{"class":"date_posted"})
	date = date_Container[0].text

	#TODO: Remake this dumb piece of code for looping like 4 more times increases the output time dummy
	content_Container = rev.find("div",{"class":"apphub_CardTextContent"})
	content_Container.div.decompose()
	for div in content_Container.findAll("div",{"class":"dynamiclink_box"}):
		div.decompose()
	for div in content_Container.findAll("div",{"class":"received_compensation"}):
		div.decompose()
	for div in content_Container.findAll("div",{"class":"refunded"}):
		div.decompose()
	for a in content_Container.findAll("a"):
		a_tag = a
		a_tag.decompose()
	content = content_Container.text.strip()

	#print ("\nRecommend: " + recommended)
	#print (date)
	#print ("User: " + user)
	#print ("Review: \n" + content)

	f.write(recommended + "," + date.replace(",","|") + "," + content.replace("," , "|") + "\n")

f.close()