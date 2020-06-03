import re
import json
import aiohttp
import asyncio
from datetime import datetime


values = {
    'megan': 48894571,
    'kelly': 48894572,
}
PARAMS = [
    ('p', 10560431),
    ('b', 0),
    ('o', ''),
    ('va', 0),
    ('cookie', 0),
    ('url', 'https://buffalonews.com/2020/06/01/vote-for-the-prep-talk-girls-athlete-of-the-week-champion/'),
]
params = lambda a, n: [*PARAMS, ('a', a), ('n', n)]
url = lambda d: f'https://polldaddy.com/n/9f7c2033b5acf7488f5e5fe7a902df43/10560431?{d}'
r = re.compile("^.*'(?P<value>[a-z0-9|]+)'.*$")

headers = {
    "accept": "*/*",
    "referer": "https://buffalonews.com/",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua": "\"\\\\Not\\\"A;Brand\";v=\"99\", \"Chromium\";v=\"84\", \"Google Chrome\";v=\"84\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 13099.14.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.21 Safari/537.36"
}

async def request(session: aiohttp.ClientSession, date: datetime):
        d = int(date.timestamp() * 1000)
        async with session.get(url(d)) as resp:
            text = await resp.text()
            match = r.match(text)
            n = match.group('value')
            a = values['megan']
            async with session.get('https://polls.polldaddy.com/vote-js.php', params=params(a, n), headers=headers) as resp:
                print(f'status: {resp.status}, {n}')


async def main():
    async with aiohttp.ClientSession() as session:
        date = datetime.now()
        while date < datetime(2020,6,5):
            date = datetime.now()
            await request(session, date)
            await asyncio.sleep(5)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
