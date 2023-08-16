import argparse
import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
}
result = []
domains = []


async def fetch_url(session, url):
    global n
    async with session.get(url, headers=header) as response:
        time.sleep(0.2)
        print(url)
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, f"https://www.beianx.cn/search/{domain}") for domain in domains]
        response = await asyncio.gather(*tasks)
        for domain, html in zip(domains, response):
            r = {}
            bs = BeautifulSoup(html, "html.parser")
            elements = bs.select(".breadcrumb + table tbody tr td")
            if len(elements) > 1:
                r['域名'] = domain
                r['主办单位名称'] = elements[1].find("a").text.strip()
                r['主办单位性质'] = elements[2].text.strip()
                r['备案号'] = elements[3].text.strip()
                r['网站名词'] = elements[4].text.strip()
                r['审核日期'] = elements[6].find("div").text.strip()
                result.append(r)
        for o in result:
            print(o)


if __name__ == "__main__":
    argparse = argparse.ArgumentParser("")
    argparse.add_argument("-l", "-file_path", dest="file_path")
    args = argparse.parse_args()
    file_path = args.file_path
    with open(file_path, "r", encoding="utf-8") as file:
        for e in file:
            e = e.strip()
            domains.append(e)
    asyncio.run(main())
