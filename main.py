import os
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

root_dir = './files/'
if not os.path.exists(root_dir):
    os.makedirs(root_dir)

r = requests.get("https://3dbuzz.com", verify=False)
with open(root_dir + 'index.html', 'wt', encoding="utf-8") as outFile:
    outFile.write(r.text)
    outFile.close()

r = requests.get("https://3dbuzz.com/index.css", verify=False)
with open(root_dir + 'index.css', 'wt', encoding="utf-8") as outFile:
    outFile.write(r.text)
    outFile.close()

soup = BeautifulSoup(r.text, features='html.parser')
series = soup.find_all('div', class_='c-series')

for entry in series:
    title = entry.find('h3').text
    title = title.replace(':', ' -')
    title = title.replace('?', '')
    title = title.replace('*', '')
    path = root_dir + title
    
    if not os.path.exists(path):
        os.makedirs(path)

        for link in entry.find_all('li'):
            href = link.find('a')['href']
            pos = href.rfind('/') + 1
            fileName = path + '/' + href[pos:]
            print('Creating file: ', fileName)
            with open(fileName, 'wb') as outFile:
                while (True):
                    print('Getting: ', href)
                    r = requests.get(href)
                    if r.status_code == 200:
                        outFile.write(r.content)
                        break
                outFile.close()
            print()
