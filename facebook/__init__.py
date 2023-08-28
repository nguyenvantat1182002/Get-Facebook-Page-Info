from bs4 import BeautifulSoup
from typing import Optional

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

    def get_likes(self) -> Optional[int]:
        soup = BeautifulSoup(self.content.text, 'html.parser')

        page_description = soup.select_one('meta[name="description"]')
        page_description = page_description['content']
        page_description = page_description[len(self.get_name()):]

        likes = re.findall(r'([\d,]+K?)\s+likes', page_description)
        if not likes:
            return None
        
        likes: str = likes[0]
        
        if likes.endswith('K'):
            likes = likes.replace('K', '')
            likes = int(likes) * 1000
        elif ',' in likes:
            likes = likes.replace(',', '')

        likes = int(likes)

        return likes
    
    def get_address(self) -> str:
        if 'maps.google.com' not in self.content.text:
            return None
        
        address = re.findall(r'"text":"([^"]*)"}},"associated_page_id"', self.content.text)
        
        return address[0]
        
    def is_verified(self) -> bool:
        return '"is_verified":true' in self.content.text
    