from bs4 import BeautifulSoup
import os
from openpyxl import Workbook

def getSoup(filepath):
    page = open(filepath, "r", encoding="utf-8")
    html = page.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup



def getSearchData(page):
    soup = getSoup(f"page{page}.html")
    data_rows= soup.find_all('div', class_="col-md-12 data")
    return data_rows
    
def getLinksToScrape(data_rows, file ):
    for i, d in enumerate(data_rows):
        name = d.find('div', class_="col-md-6")
        file.write('https://dnb.com'+name.find('a').get('href')+'\n') 

def getBaseLinkInfo(data_rows, data):
    for i, d in enumerate(data_rows):
        data.append([])
        name = d.find('div', class_="col-md-6")
        data[i+1].append(name.find('a').get_text(strip=True).replace('\n', ' '))
        loc = name.find_next('div')
        loc_child = loc.findChild('div')
        if loc_child:
            loc_child.decompose()
        data[i+1].append(' '.join(loc.get_text().replace('\n', ' ').replace(R'\xa0', ' ').split()))
        rev = loc.find_next('div', class_="col-md-2 last")
        rev_child = rev.findChild('div')
        if rev_child:
            rev_child.decompose()
        data[i+1].append(rev.get_text(strip=True))
   
def getCompanyInfo(data_rows, data):
    for i, d in enumerate(data_rows): 
        name = d.find('div', class_="col-md-6")   
        filename = name.find('a').get('href').split('.')[1]
        print(f"checking a file {i}")
        filepath= os.path.join('companies', filename)
        soup = getSoup(filepath)
        business_name = soup.find(attrs={'data-tracking-name':'Doing Business As:'})
        def addToData(thing):
            if(thing):
                text = thing.get_text(strip=True).replace('See more contacts', '').split(':')
                if(len(text)) > 1:
                    text = text[1]
                else:
                    text = text[0]
                data[i+1].append(text)
            else:
                data[i+1].append('')
                'nothing added'
        addToData(business_name)
        address = soup.find(attrs={'name':'company_address'})
        addToData(address)
        website = soup.find(id='hero-company-link')
        
        addToData(website)
        key_principal = soup.find(attrs={'name':"key_principal"})
        addToData(key_principal)
        if key_principal:
            contact_soup = getSoup(os.path.join('contacts', filename+'-contacts'))
            position = contact_soup.find(class_="position sub")
        addToData(position)

if __name__ == "__main__":   
    data = [['Name', 'Location', 'Revenue', 'Business Name', 'Address', 'Website', 'Key Principal', 'Position']]
    pages = range(9, 14)    #current pages scraped and stored in directories, refer to html files pageX.html for which pages to store
    file = open("links_to_scrape.txt", 'w', encoding='utf-8') 
    data_rows=[]
    for page in pages:
        data_rows += getSearchData(page)
    
    getBaseLinkInfo(data_rows, data)
    print(len(data_rows)) 
    print(len(data))  
    input('continue? ')
    getCompanyInfo(data_rows, data)
    print(len(data))   
    input('continue? ')

    wb = Workbook()
    ws = wb.active
    ws.title = "Companies"

    for row in data:
        ws.append(row)
    wb.save("companies.xlsx")