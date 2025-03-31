# %%

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.residentevildatabase.com/personagens/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_gid=GA1.2.727671666.1743369209; __gads=ID=90e38375b84c9433:T=1743369208:RT=1743371570:S=ALNI_MZUf3HUmsmSkcR1W2WjVBBhwrvn2A; __gpi=UID=0000108994352061:T=1743369208:RT=1743371570:S=ALNI_MYjT1Hb0BOak0Ky9ZpITnsbsl8JkA; __eoi=ID=27319472821163ce:T=1743369208:RT=1743371570:S=AA-Afjb2FezeL19PD5iVbCp1X8Yh; _ga_DJLCSW50SC=GS1.1.1743371568.2.1.1743371574.54.0.0; _ga_D6NF5QC4QT=GS1.1.1743371568.2.1.1743371574.54.0.0; _ga=GA1.2.1078752623.1743369204; FCNEC=%5B%5B%22AKsRol8w8lt5ROGX3FfjpCqgr1lJfHk1mivSxwRTecUGEHPq3FVDQNPqIfhfjjadD4tv4aHXKkMUCYv8qamKBP4h5Fr4lOfYeG3cb5LmvFSdqxFCJQRUDngDesJLC6mNtLX8x1U6PnLTPCEXmas0n9nQ7zbcqKbUwQ%3D%3D%22%5D%5D',
    }

def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp

def get_basic_infos(soup):
    div_page = soup.find('div', class_ = 'td-page-content')
    paragrafo = div_page.find_all('p')[1]
    ems = paragrafo.find_all('em')
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(':')
        chave = chave.strip(' ')
        data[chave] = valor.strip(' ')

    return data

def get_aparicoes(soup):
    lis = soup.find('div', class_ = 'td-page-content').find('h4').find_next().find_all('li')

    aparicoes = [i.text for i in lis]
    return aparicoes

def personagem_infos(url):
    resp = get_content(url)

    if resp.status_code != 200:
        print('Não foi possível obter os dados.')
        return {}
    
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data['Aparicoes'] = get_aparicoes(soup)
        return data
    
def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)

    ancoras = (soup_personagens.find('div', class_='td-page-content')
    .find_all('a'))

    links = [i['href'] for i in ancoras]
    return links


# %%
url = 'https://www.residentevildatabase.com/personagens/ada-wong/'

personagem_infos(url)

links = get_links()
data = []
for i in tqdm(links):
    d = personagem_infos(i)
    d['link'] = i
    data.append(d)

# %%

df = pd.DataFrame(data)
df

df.to_parquet('dados_re.parquet', index=False)

df_new = pd.read_parquet('dados_re.parquet')

df_new

