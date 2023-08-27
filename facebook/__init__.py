from bs4 import BeautifulSoup

import requests
import re


class Page:
    def __init__(self, page_id: str, user_agent: str):
        self.page_id = page_id
        self.session = requests.Session()

        self.session.headers.update({
            'User-Agent': user_agent,
            'Sec-Fetch-Site': 'none',
            'Accept-Language': 'en-US,en;q=0.9'
        })

        self.content = self.session.get(
            f'https://www.facebook.com/{self.page_id}/',
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            }
        )

    def get_name(self) -> str:
        soup = BeautifulSoup(self.content.text, 'html.parser')
        title = soup.select_one('meta[property="og:title"]')

        return title['content']

    def get_likes(self) -> str:
        soup = BeautifulSoup(self.content.text, 'html.parser')
        page_description = soup.select_one('meta[property="og:description"]')
        page_description = page_description['content']

        likes = re.findall(r'(\d+(?:,\d{3})*)(?:\s+likes)', self.content.text)
        if not likes:
            return None

        return likes[0]
    
    def get_address(self) -> str:
        address = re.findall(r'"text":"(.*?)"', self.content.text)
        
        if 'maps.google.com' not in self.content.text:
            return None
        
        return address[4]
        
    def is_verified(self) -> bool:
        return '"is_verified":true' in self.content.text
    