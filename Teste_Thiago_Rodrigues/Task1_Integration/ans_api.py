import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

def get_latest_quarters(limit=3):
    """
    Crawls the ANS site to find the last 3 available quarters.
    Returns a list of tuples (year, quarter, download_url)
    """
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all year folders (4 digits)
    years = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and re.match(r'^\d{4}/?$', href):
            years.append(href.strip('/'))
    
    # Sort years descending
    years.sort(reverse=True)
    
    quarters_found = []
    for year in years:
        year_url = urljoin(BASE_URL, year + '/')
        resp = requests.get(year_url)
        if resp.status_code != 200:
            continue
            
        y_soup = BeautifulSoup(resp.text, 'html.parser')
        # Look for ZIP files like 1T2024.zip or subfolders
        year_quarters = []
        for q_link in y_soup.find_all('a'):
            q_href = q_link.get('href')
            if q_href and q_href.endswith('.zip'):
                # Extract quarter and year from filename like 1T2024.zip
                match = re.search(r'(\d)T(\d{4})', q_href)
                if match:
                    q_num = match.group(1)
                    q_year = match.group(2)
                    year_quarters.append((q_year, q_num, urljoin(year_url, q_href)))
        
        # Sort quarters in year descending
        year_quarters.sort(key=lambda x: x[1], reverse=True)
        quarters_found.extend(year_quarters)
        
        if len(quarters_found) >= limit:
            break
            
    return quarters_found[:limit]

def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        
    filename = os.path.basename(url)
    dest_path = os.path.join(dest_folder, filename)
    
    print(f"Downloading {url} to {dest_path}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return dest_path
