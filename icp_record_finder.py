import argparse
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
}
result = []
domains = []


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get?type=https").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


async def fetch_url(session, url):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 1:
        try:
            async with session.get(url, headers=header, proxy=f"http://{proxy}") as response:
                print(url)
                return await response.text()
        except Exception:
            retry_count = -1
    delete_proxy(proxy)
    return None


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, f"https://www.beianx.cn/search/{domain}") for domain in domains]
        response = await asyncio.gather(*tasks)
        for domain, html in zip(domains, response):
            if response:
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
