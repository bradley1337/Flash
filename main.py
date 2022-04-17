import os
import asyncio
import random
import ctypes
import json
import sys
import time

print("\n[+] Flash has started...
try:
  import requests
except ImportError:
    os.system('pip install requests')
    import requests
try:
  import aiohttp
except ImportError:
    os.system('pip install aiohttp')
    import aiohttp
 
class bot:

    def __init__(self):
        self.channel = str(input('Channel: ')).lower()
        self.amount = int(input('Amount: '))
        try:
            headers = {'Client-Id': 'abe7gtyxbr7wfcdftwyi9i5kej3jnq', 'Accept': 'application/vnd.twitchtv.v5+json', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}
            cid_req = requests.get(f'https://api.twitch.tv/kraken/users?login={self.channel}', headers=headers).json()
            self.cid = cid_req['users'][0]['_id']
        except Exception as error:
            if len(cid_req['users']) == 0:
                print('Invalid Channel')
            else:
                print(cid_req)
                print(error)
            time.sleep(2)
            os._exit(0)
        self.oauth = []
        self.load_oauth()

        if len(self.oauth) <= self.amount:
            self.amount = len(self.oauth)

        print(f'Sending {self.amount} twitch followers to {self.channel}!')
        

    def load_oauth(self):
        with open('tokens.txt', 'r', encoding='utf-8', errors='ignore') as f:
            for x in f.readlines():
                self.oauth.append(x.replace('\n', ''))
        print(f'Loaded {str(len(self.oauth))} tokens!')

    async def bot(self, session):
        try:
            token = self.oauth.pop(random.randint(0, len(self.oauth)-1)).split(':')[-1]
            data = '[{"operationName":"FollowButton_FollowUser","variables":{"input":{"disableNotifications":false,"targetID":"' + self.cid + '"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"3efee1acda90efdff9fef6e6b4a29213be3ee490781c5b54469717b6131ffdfe"}}}]'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
                'Origin': 'https://www.twitch.tv',
                'Referer': 'https://www.twitch.tv/' + self.channel,
                'Content-Type': 'text/plain;charset=UTF-8',
                'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                'Authorization': 'OAuth ' + token,
                'Accept-Language': 'en-US'
            }
            async with session.post('https://gql.twitch.tv/gql', headers=headers, data=data) as r:
                text = await r.text()
                print(text)
        except Exception as e:
            print(str(e))

    async def start(self):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.bot(session) for _ in range(self.amount)])
        await asyncio.sleep(1)
        os._exit(0)

if __name__ == '__main__':
    try:
      ctypes.windll.kernel32.SetConsoleTitleW('Twitch Follow Bot')
    except:
      pass
    main = bot()
    asyncio.run(main.start())
