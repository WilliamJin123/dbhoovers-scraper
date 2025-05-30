
import requests, time, random
import urllib.parse
from scraperBS import getSearchData, getLinksToScrape
TOKEN = "" #scrape.do api token here


def getSearchPages(start = 0, end = 20): #inclusive start end
    start = max(0, start)
    end = min(20, end)
    LINK = "https://www.dnb.com/business-directory/company-information.food_manufacturing.ca.ontario.html?page="
    
    for i in range(start, end+1):
        to_scrape = LINK + str(i)
        targetUrl = urllib.parse.quote(to_scrape)
        url = "http://api.scrape.do/?token={}&url={}".format(TOKEN, targetUrl)
        response = requests.request("GET", url)

        html_file = open(f"page{i}.html", "w", encoding="utf-8")
        html_file.write(response.text)
        html_file.close()



def getCompanyWebsiteHtml():
    links = open('links_to_scrape.txt', 'r', encoding='utf-8')
    lines = links.readlines()
    links.close()
    for link in lines:
        targetUrl = urllib.parse.quote(link.replace('\n', ''))
        print(targetUrl)
        url = "http://api.scrape.do/?token={}&url={}".format(TOKEN, targetUrl)
        
        response = requests.request("GET", url)
        company = open(f'companies/{link.split('.')[2]}', 'w', encoding='utf-8')
        company.write(response.text)
        company.close()
        
        targetUrl = urllib.parse.quote(link.replace('\n', '')+'#contact-anchor')
        print(targetUrl)
        url = "http://api.scrape.do/?token={}&url={}".format(TOKEN, targetUrl)
        
        response = requests.request("GET", url)
        company = open(f'contacts/{link.split('.')[2]}-contacts', 'w', encoding='utf-8')
        company.write(response.text)
        company.close()
        
if __name__ == "__main__":
    getSearchPages(13, 13)
    data_rows = getSearchData(13)
    file = open("links_to_scrape.txt", 'w', encoding='utf-8') 
    getLinksToScrape(data_rows, file)
    file.close()
    getCompanyWebsiteHtml()