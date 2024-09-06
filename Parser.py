import requests
from bs4 import BeautifulSoup
import os
url = 'https://russrivership.ru/ships'
response = requests.get(url)
html = response.content
import re
soup = BeautifulSoup(html, 'html.parser')

main_block = soup.find('div', class_='mainDV')
links = []
titls = []
if main_block:

    maintext_block = main_block.find('div', class_='maintextDV')
    if maintext_block:
        
        link_tags = maintext_block.find_all('a', class_='mainlink')
        
        for link in link_tags:
            href = link.get('href')
            full_link = "https://russrivership.ru" + href
            links.append(full_link)
            
            text = link.get_text(strip=True) 
            titls.append(text)
else:
    print("Блок mainDV не найден")

def clean_filename(filename):
    # Удаляем все управляющие символы (\r, \n и т.д.)
    filename = filename.replace('\r', '').replace('\n', '').strip()
    # Удаляем символы, запрещенные в именах файлов на Windows
    return re.sub(r'[\\/*?:"<>|]', "", filename)
for i, ship_url in enumerate(links):
    title = titls[i]

    folder_name = clean_filename(title.replace(" ", " "))  
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    ship_response = requests.get(ship_url)
    ship_html = ship_response.content
    ship_soup = BeautifulSoup(ship_html, 'html.parser')

    pdf_link = ship_soup.find_all('a', class_='pdflink')
    for link_p in pdf_link:
        if link_p:
            pdf_href = link_p.get('href')
            pdf_url = "https://russrivership.ru" + pdf_href

            pdf_response = requests.get(pdf_url)
            text_pdf = link_p.get_text(strip=True)

  
            pdf_file_name = clean_filename(text_pdf) + ".pdf"
            pdf_file_path = os.path.join(folder_name, pdf_file_name)  
            
          
            with open(pdf_file_path, 'wb') as f:
                f.write(pdf_response.content)

            print(f"Файл {pdf_file_name} успешно скачан в папку {folder_name}")
