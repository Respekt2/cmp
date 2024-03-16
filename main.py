from bs4 import BeautifulSoup
import requests
import json

url = 'https://cpm-digital.ru/expositions/exposition/45-cpm-2024-spring.html'

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, 'lxml')

contacts_people_result = []
list_link = []
x = 0
while True:
    url_2 = f'https://cpm-digital.ru/?Itemid=132&option=com_expo&view=exposition&task=viewexposition&id=45&ajaxScroll=1&start={x}'
    req_2 = requests.get(url_2, headers=headers)
    src_2 = req_2.text
    soup_2 = BeautifulSoup(src_2, 'lxml')
    x += 48
    title = soup_2.find_all(class_='span3')
    links_found = False
    for i in title:
        link = i.find('a')
        href = link.get('href')
        if href:
            links_found = True
            link_link = f'https://cpm-digital.ru{href}'
            list_link.append(link_link)

    if not links_found:
        break

for country in list_link:
    req_country = requests.get(country, headers=headers)
    src_country = req_country.text
    soup_country = BeautifulSoup(src_country, 'lxml')

    title = soup_country.title.text
    company_site = soup_country.find(class_='company_site')
    if company_site:
        web_site = company_site.find('a', {'target': '_blank'})
        if web_site:
            web = web_site.get('href')
        else:
            web = '-'    

    company_email = soup_country.find(class_='company_email')
    try:
        if company_email:
            teg_a_email = company_email.find('a')
            list_email=teg_a_email.text 
    except AttributeError:
        list_email = '-'

    company_nomer = soup_country.find_all(class_='company_email')
    try:
        if len(company_nomer) > 1:
            teg_a_nomer = company_nomer[1].find('a')
            list_nomer=teg_a_nomer.text      
    except AttributeError:
        list_nomer = '-' 



    if company_site and company_email:
        contacts_people_result.append({
            'Title': title,
            'Company Site': web if web else "",
            'E-mails': list_email if list_email else '-',
            'nomer': list_nomer if list_nomer else '-'
        })
    else:
        print(f"No data found for {country}")

with open(f'cmp/cmp.json', 'w', encoding='utf-8') as file:  
    json.dump(contacts_people_result, file, indent=4, ensure_ascii=False)
