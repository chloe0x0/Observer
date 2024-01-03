import os
import argparse
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List

TARGET_PATH = "https://transcripts.foreverdreaming.org/viewforum.php?f=364"
SITE_URL = "https://transcripts.foreverdreaming.org/"

def get_episode_urls():
    ''' Will grab all the urls for the transcripts from the TARGET_PATH'''
    r = requests.get(TARGET_PATH)
    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.findAll('a', class_="topictitle")
    rows = list(filter(lambda x : not x.text.startswith('Updates: '), rows))
    return [row for row in rows]

def download_transcripts(download_path: str, urls: List[Tag]):
    '''
    Given a download path and a list of episode urls download them.
        path
        |____S1
        |
        |_____S2
        .
        .
        .
    '''
    for url in urls:
        r = requests.get(SITE_URL + '/' + url.get('href'))
        soup = BeautifulSoup(r.content, 'html.parser')
        text = soup.find('div', class_="content").text
        # grab out the Season number (first 5 characters)
        season_idx = url.text[:2]
        episode_idx = url.text[3:5]
        path = os.path.join(download_path, season_idx)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, episode_idx+'.txt'), 'w', encoding='utf-8') as outfile:
            outfile.write(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Observer",
        description="A web scraper for Rick and Morty transcripts"
    )

    parser.add_argument("--path", '--p', type=str, dest="path", required=True)
    args = parser.parse_args()

    urls = get_episode_urls()
    download_transcripts(args.path, urls)