#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   英雄联盟.py
@Time    :   2023/02/12 16:39:34
@Author  :   Codebat
@Version :   1.0
@Contact :   hofong.chang@gmail.com
'''

import asyncio
import aiohttp
import os
import time


class Crawl_img():
    def __init__(self):
        self.url = 'https://pvp.qq.com/web201605/js/herolist.json'
        self.skin_url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

    async def spider_img(self, session, ename, cname):
        for i in range(1, 10):
            response = await session.get(self.skin_url.format(ename, ename, i))
            if response.status == 200:
                content = await response.read()
                with open('picture/' + cname + '-' + str(i) + '.jpg', 'wb')as f:
                    f.write(content)
                    print('downloading{}skin{}'.format(cname, i))
            else:
                break

    async def run(self):
        async with aiohttp.ClientSession(headers=self.headers)as session:
            response = await session.get(self.url)
            wzry_data = await response.json(content_type=None)
            print(wzry_data)
            tasks = []
            for i in wzry_data:
                ename = i['ename']
                cname = i['cname']
                # create
                res = self.spider_img(session, ename, cname)
                task = asyncio.create_task(res)
                tasks.append(task)

            await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    if not os.path.exists('picture'):
        os.mkdir('picture')

    wzry = Crawl_img()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wzry.run())
    print('time_spent:', time.time()-t1)
