import json
import random
from typing import Dict, List, OrderedDict
from unittest import result
import requests as _requests
import asyncio
import aiohttp
import time

def _generate_markets(searchTerm: str) -> json:
    url = "https://www.rewe.de/api/marketsearch"

    querystring = {"searchTerm":searchTerm}

    headers = {"cookie": "mtc=s%253AIFMzL9Oul6jfdAJbQhy%252B2PQwXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJnBheWJhY2stZWNvdXBvbi1hcGkucGF5YmFjay1yZXdlLW5ld3NsZXR0ZXJEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlciphYmhvbHNlcnZpY2UtcmVsb2FkZWQsb2ZmZXItZGV0YWlscy10cmFja2luZz5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSZwYXliYWNrLWNhcmQtY2hhbmdlJG1lbmdlbnJhYmF0dGllcnVuZypwYXliYWNrLXRhcmdldGVkLWJ1cm4oc3dpdGNoLXJ1bGUtaW5zaWdodHMocGF5YmFjay12b3VjaGVyLXdhbGwocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmcod29va2llZXMtcGlja3VwLXBhZ2UmbWFya3RzZWl0ZS1yZWxvYWRlZDpwcm9kdWN0bGlzdC1uZXctbW9iaWxlLWZpbHRlciBwYXliYWNrLWV2b3VjaGVyQGluaS0zNjc4LWRpc21hbnRsaW5nLW1hcmtldHBsYWNlFG5ldy1oZWFkZXI6cGF5YmFjay10YXJnZXRlZC1ib251cy1jb3Vwb242aW5pLTM4MTItaGlkZS1yZWd1bGFyLXByaWNlAAAA.B0hbv5i%252Bw6fZqa2zekZ3EMgvK0pL5KZNXLkC1myDsq0; MRefererUrl=direct; _rdfa=s%253Aafe95d8f-c902-4ac0-af9e-38aefb723c36.TTrHhpPQLiUsRmu7l8ebIwwIQx4cJvvnUmJgh9xFjlc; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiI3ZjM4NjhjOTM2OGRhZDYyODBhNzkxZDg4YWU3ODJhYTZiODY4NjdkYmM0ZmE2ODYwYzJlNWFiYWY2YzFkMjIzMjgxNTI3MTFiMWE0NjBmZGNhMGY3YzRlMDljMTJlMTc5ZDBiYWZlMDA0ZmY3OGRiZDhlNWFjN2QyZDU0ZGY2YzAxMTAyMjBiMDQzMWI3ZGViMTUwOGQxZjQ1ZjViZTM3ZTI1OTYwZWYwZDVmZWNhZmNiMjhlZTBlYTFhNzFjYTk4Y2Y1YmU4YjdiNDExMmVlZjVlZjYwYWQ5NzM1MzNmYmVlN2JhNWRkOTU4NzFmMGE5MDIwOGMxZmVmZGYxYjQ0IiwiaWF0IjoxNjU3MjkyMzM5LCJleHAiOjE2NTcyOTI5Mzl9.q96wiHdUZ8um4t55j88Nz6YT1VHSiNk3EMqwcCAL2zFpSR5XLA2zDOAdhICj8joKFvZM5p5SZf0jp-0SUAbyrA; __cf_bm=wJuUr9JdNAhYifAS2HNhM9qOquTBRJMv46IN.a7sBms-1657291910-0-AUEgDfYdjpZeq8LSjF3m%2BvbbljaPy8ptzwbqoIUnGEpa%2Fl6NafMGjVU%2BHZYmqC2oFXGjNkyfmoTvLuP9gp82%2BcU%3D; __cfruid=cde6fd47a76da21e1b5d79fc82beee179309320e-1657291910; _cfuvid=nEKf.zWiV3_hnd8SdLCP0WokLzKKQxx_0J3Dsz_wgwc-1657291910287-0-604800000"}

    r = _requests.request("GET", url, headers=headers, params=querystring)
    print(r.content)
    data = r.json()
    return data

def _all_offers(searchTerm: str) -> Dict:
    markets = _generate_markets(searchTerm)
    rawOffers = dict()
    n = 1
    for market in markets:
        marketId = market["wwIdent"]
        marketName = market["marketHeadline"]
        marketAdress = market["contactStreet"] + " " + market["contactZipCode"]
        url = f"https://www.rewe.de/api/all-stationary-offers/{marketId}"

        payload = ""
        headers = {"cookie": "mtc=s%253AIFMzL9Oul6jfdAJbQhy%252B2PQwXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJnBheWJhY2stZWNvdXBvbi1hcGkucGF5YmFjay1yZXdlLW5ld3NsZXR0ZXJEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlciphYmhvbHNlcnZpY2UtcmVsb2FkZWQsb2ZmZXItZGV0YWlscy10cmFja2luZz5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSZwYXliYWNrLWNhcmQtY2hhbmdlJG1lbmdlbnJhYmF0dGllcnVuZypwYXliYWNrLXRhcmdldGVkLWJ1cm4oc3dpdGNoLXJ1bGUtaW5zaWdodHMocGF5YmFjay12b3VjaGVyLXdhbGwocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmcod29va2llZXMtcGlja3VwLXBhZ2UmbWFya3RzZWl0ZS1yZWxvYWRlZDpwcm9kdWN0bGlzdC1uZXctbW9iaWxlLWZpbHRlciBwYXliYWNrLWV2b3VjaGVyQGluaS0zNjc4LWRpc21hbnRsaW5nLW1hcmtldHBsYWNlFG5ldy1oZWFkZXI6cGF5YmFjay10YXJnZXRlZC1ib251cy1jb3Vwb242aW5pLTM4MTItaGlkZS1yZWd1bGFyLXByaWNlAAAA.B0hbv5i%252Bw6fZqa2zekZ3EMgvK0pL5KZNXLkC1myDsq0; MRefererUrl=direct; _rdfa=s%253Aafe95d8f-c902-4ac0-af9e-38aefb723c36.TTrHhpPQLiUsRmu7l8ebIwwIQx4cJvvnUmJgh9xFjlc; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiI3ZjM4NjhjOTM2OGRhZDYyODBhNzkxZDg4YWU3ODJhYTZiODY4NjdkYmM0ZmE2ODYwYzJlNWFiYWY2YzFkMjIzMjgxNTI3MTFiMWE0NjBmZGNhMGY3YzRlMDljMTJlMTc5ZDBiYWZlMDA0ZmY3OGRiZDhlNWFjN2QyZDU0ZGY2YzAxMTAyMjBiMDQzMWI3ZGViMTUwOGQxZjQ1ZjViZTM3ZTI1OTYwZWYwZDVmZWNhZmNiMjhlZTBlYTFhNzFjYTk4Y2Y1YmU4YjdiNDExMmVlZjVlZjYwYWQ5NzM1MzNmYmVlN2JhNWRkOTU4NzFmMGE5MDIwOGMxZmVmZGYxYjQ0IiwiaWF0IjoxNjU3MjkyMzM5LCJleHAiOjE2NTcyOTI5Mzl9.q96wiHdUZ8um4t55j88Nz6YT1VHSiNk3EMqwcCAL2zFpSR5XLA2zDOAdhICj8joKFvZM5p5SZf0jp-0SUAbyrA; __cf_bm=wJuUr9JdNAhYifAS2HNhM9qOquTBRJMv46IN.a7sBms-1657291910-0-AUEgDfYdjpZeq8LSjF3m%2BvbbljaPy8ptzwbqoIUnGEpa%2Fl6NafMGjVU%2BHZYmqC2oFXGjNkyfmoTvLuP9gp82%2BcU%3D; __cfruid=cde6fd47a76da21e1b5d79fc82beee179309320e-1657291910; _cfuvid=nEKf.zWiV3_hnd8SdLCP0WokLzKKQxx_0J3Dsz_wgwc-1657291910287-0-604800000"}

        r = _requests.request("GET", url, data=payload, headers=headers)
        raw = r.json()
        rawOffers[n] = {
            "market": marketName + " " + marketAdress,
            "id": marketId,
            "offers": raw["filters"][0]["categories"]
        }
        
        n += 1
    return rawOffers

def get_tasks(session, ids):
    headers_list = [
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIO1w8ex4JyTsZxHT5MVlBY80KHBheWJhY2stdm91Y2hlci13YWxsRHByb2R1Y3RsaXN0LW1vYmlsZS1jYXRlZ29yeS1maWx0ZXImbWFya3RzZWl0ZS1yZWxvYWRlZDZwcm9kdWN0bGlzdC1jYXRlZ29yeS10ZWFzZXI6cHJvZHVjdGxpc3QtbmV3LW1vYmlsZS1maWx0ZXIqcGF5YmFjay10YXJnZXRlZC1idXJuJHRyYm8tYmFubmVyLWRlbG1vZCZwYXliYWNrLWVjb3Vwb24tYXBpXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrIHBheWJhY2stZXZvdWNoZXIqYWJob2xzZXJ2aWNlLXJlbG9hZGVkOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uPnByb2R1Y3RsaXN0LW5hdmlnYXRpb24tdHJhY2tpbmc2aW5pLTM4MTItaGlkZS1yZWd1bGFyLXByaWNlKm1vYmlsZS1wYXliYWNrLWFwaUtleSRtZW5nZW5yYWJhdHRpZXJ1bmcocHJvZHVjdGxpc3QtY2l0cnVzYWRAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UmcGF5YmFjay1jYXJkLWNoYW5nZTRwcm9kdWN0bGlzdC1uZXctZGVhbHMtcGFnZShzd2l0Y2gtcnVsZS1pbnNpZ2h0cyxvZmZlci1kZXRhaWxzLXRyYWNraW5nKHdvb2tpZWVzLXBpY2t1cC1wYWdlLm5ldy1uYXZpZ2F0aW9uLXRyYWNraW5nLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyFG5ldy1oZWFkZXIAAAA%3D.YsC8Ukzxx1gXfe%2FiYgiINXLSSDIwbxh1yHyvi005D24; MRefererUrl=direct; _rdfa=s%3Aa331597f-33d8-4b39-aa1b-c9230e28db0e.WQQAWrl5VAk%2FInWwkEhEWB%2FMzMZ8%2FzoHi8B85Pc3Xmw; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJlMTJiYTBmM2ExMDIyZjM5ZGM0NjcyN2QwN2MwYzcwMWNlMWY2NjJmMDQyNzZjZDI5NDY0OGFiMWRlNWRjNGRmNjY3ZTM4M2Y5NjU5MzUyZDBlMDU2MzliY2YwMGMyMGQ1ZTFmYzAwMmNmMzc3N2Q0OThkNTgxZDA3MTdhZjdmNmY0ODMxNjM1MmM0MjBhNTk2MWFiMTBiM2IyYWYzNTI5ZTJmMzFiYTNiMTNhOWQ2MjViYTc3ZjMzMjk3ZmZjYTZkMDI0MTUyYWNjMDJmZmIzNzVlMGExMjg5YmQ4ZDc4N2E3MTA4OGVmYWUwMTI2MThiM2JjOWFiMmE0NTg5YTc1IiwiaWF0IjoxNjU3ODI0NTMyLCJleHAiOjE2NTc4MjUxMzJ9.9D3t0PZwSmaTtScdo9mBUQuZJ04_kJXTzS3RaUi_Xf5XKYRFZ5DeaYD8EgHywqTdodVD078IGJzLQR7PCKv0eg; __cf_bm=nUUWCx6paM9w2MDyyv2G31r7W9Rab5WHI3CdVKvKqPw-1657824532-0-AbTeVyOo/fPZV2hNG6MD/HK6oYvmcJVNWK8AJjdnIZdwhcvOpcX6QCgN0juEPwW9Vl1eFfoKnyws2NfBdj/2e+c=; __cfruid=0ff4a3204604bec09f9cde915bde1d328bf1b1d1-1657824532; _cfuvid=aaeGJb8SYJeUaSzo1KDyx0IzcmyEgyu3OPsC3.ZFXmo-1657824532318-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIKWpHSIKOXaVTEymBHEQLtE2OHByb2R1Y3RsaXN0LXRlc3RpbmctY2l0cnVzYWQoc3dpdGNoLXJ1bGUtaW5zaWdodHMocGF5YmFjay12b3VjaGVyLXdhbGwUbmV3LWhlYWRlciZtYXJrdHNlaXRlLXJlbG9hZGVkXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrJnBheWJhY2stY2FyZC1jaGFuZ2VAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2VEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlcjRwcm9kdWN0bGlzdC1uZXctZGVhbHMtcGFnZSRtZW5nZW5yYWJhdHRpZXJ1bmc6cGF5YmFjay10YXJnZXRlZC1ib251cy1jb3Vwb24gcGF5YmFjay1ldm91Y2hlcih3b29raWVlcy1waWNrdXAtcGFnZShwcm9kdWN0bGlzdC1jaXRydXNhZCphYmhvbHNlcnZpY2UtcmVsb2FkZWQ2aW5pLTM4MTItaGlkZS1yZWd1bGFyLXByaWNlLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyEHJld2Utc3NvKm1vYmlsZS1wYXliYWNrLWFwaUtleSpwYXliYWNrLXRhcmdldGVkLWJ1cm4%2BcHJvZHVjdGxpc3QtbmF2aWdhdGlvbi10cmFja2luZyZwYXliYWNrLWVjb3Vwb24tYXBpLm5ldy1uYXZpZ2F0aW9uLXRyYWNraW5nLG9mZmVyLWRldGFpbHMtdHJhY2tpbmc2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyAAAA.mOAq%2B3lpY98iKJYGYDwNhdd21Fd28Ua5kGLPHoGrrw4; MRefererUrl=direct; _rdfa=s%3A5ad961a7-c97b-4896-b9d5-9e3fa2b7bee6.RNJ3hptGCiBAZIWSNY%2FaHUEpJR0kql4opZIEXf7Orjw; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJjMzg0MmMwMDgyYjczYTgwMjE3OWY0NWFjOWM2MmQ0MWI5NGYxZjFlM2E3Y2IxZDY5ZTA4MDFjOTY0MTdlNThjNmU0NTViMTAyZjZhNDRkNGRjOGQ5ZWJmMmZmOTA0MzMzNjE4YjY4MzA0MmE4OTVlMTY1NjRhOTZhNzg0ZGJkY2JkYzM1NmFhZDdjZjgwYWE3NTFjZTlhMDdiMjk0MmZmZDM2MDM4OTA4ZmJhNDA1MDg5ZmNhZmQzZTVjNWM5ODRiMDE5NTg2NGQ5ODYxYTc3NDk4NDc5MTBjMDhlMmEzNDlkMDQwNjZkNDRmYjgyODU3ZWVmOGZiZDA5NDk1NDdhIiwiaWF0IjoxNjU3ODI0NjkxLCJleHAiOjE2NTc4MjUyOTF9.sV9eAJcWyEoSHpN9ICSHTskWPPjK5uAJeM87yStusn0pR4Ve6mHQkrjF3VvelxOEOr_QDUtSPGB-LNPKd2Wh9w; __cf_bm=G2d0F8_R2nSBze2DhimlIEX_trRSBFVesD_pGXSxWZI-1657824691-0-ARZgKMqhkJXjlbDex9/FhrhABrFEFyA2vrsE0wSLeXwgQ8rJE4Yb8IjGlZcpQFddjUuY1HvCJcUAPT14PZa8A9E=; __cfruid=46f8ddf2e24f6634a03c8896493869f54cc892a0-1657824691; _cfuvid=7NFlvd89w8oQkWC3l.m74Al0vp90UOciHNOUT99Hpsw-1657824691866-0-604800000',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'mtc=s%3AIJYUm%2BccyPnD5ZkTulJeA9I0OHByb2R1Y3RsaXN0LXRlc3RpbmctY2l0cnVzYWQucGF5YmFjay1yZXdlLW5ld3NsZXR0ZXI2aW5pLTM4MTItaGlkZS1yZWd1bGFyLXByaWNlKm1vYmlsZS1wYXliYWNrLWFwaUtleSBwYXliYWNrLWV2b3VjaGVyJG1lbmdlbnJhYmF0dGllcnVuZy5uZXctbmF2aWdhdGlvbi10cmFja2luZyxvZmZlci1kZXRhaWxzLXRyYWNraW5nFG5ldy1oZWFkZXI6cHJvZHVjdGxpc3QtbmV3LW1vYmlsZS1maWx0ZXImcGF5YmFjay1jYXJkLWNoYW5nZSh3b29raWVlcy1waWNrdXAtcGFnZUBpbmktMzY3OC1kaXNtYW50bGluZy1tYXJrZXRwbGFjZShzd2l0Y2gtcnVsZS1pbnNpZ2h0cyhwYXliYWNrLXZvdWNoZXItd2FsbCphYmhvbHNlcnZpY2UtcmVsb2FkZWQ%2BcHJvZHVjdGxpc3QtbmF2aWdhdGlvbi10cmFja2luZyZtYXJrdHNlaXRlLXJlbG9hZGVkXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlKnBheWJhY2stdGFyZ2V0ZWQtYnVybihwcm9kdWN0bGlzdC1jaXRydXNhZCZwYXliYWNrLWVjb3Vwb24tYXBpRHByb2R1Y3RsaXN0LW1vYmlsZS1jYXRlZ29yeS1maWx0ZXI6cGF5YmFjay10YXJnZXRlZC1ib251cy1jb3Vwb242cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyAAAA.UbfwhMAqj%2BqQn%2BWcgbSciio7%2BbdzCU4zlPtxjDOgeWA; MRefererUrl=direct; _rdfa=s%3A2aad1729-52c8-490f-b687-eec51e1555f8.1xAPtInjUItN7ExQXdGRrHhi4ntaXSzl8fbepCioWfw; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiI5M2ZkZGRhMmJhOWYyOTdlMjlmZGY5ODExODgwYzc1Yjc1YjNlMzcxZWUyZmY5NjdkNDgxYTc4ZDBhODU4YzYzNTJhMGYwMDAwYTZmM2VhMjczNGY5NGY0MWZjZWRmMmRlMTA0YjA5YTc0ZGQzMDQyZTkxZDlmNGU2MTViNmYxZDIwNmMwMTIxOTEwZGRkZTFkNTZiYzdmNmM5ZTdhN2FkYmQ5ZWRkNmMyNjg5NWMwMDNmZjllYjhlOWU1ZTk3ZjMzNDRlOGJmNjhiOGJiMTBiYjVhNmMyZGY5NjljOWY1ZTA3Y2E0MTcyNmNmNDMzNGQwMTIyMGIxNGE5ZWEzOWNjIiwiaWF0IjoxNjU3ODI0ODUzLCJleHAiOjE2NTc4MjU0NTN9.mJISI_TJqHEGMX7h9aRbfewiuC6xz1TN3Qt2KKnuN0hHsAu3CoKV0zQQNp4psW13nMQGKaTMpQivPYRzq1wMCg; __cf_bm=Ea.XIrwuXExk6.wJMFNp_D0kPEONAbJ3l4_bQjaxDcE-1657824853-0-Aaz7X+kDBZ3Cvi9KL7uqrPPqifNPmqfTKeVPDhnxJO9KccxjjhhZesU/Re7EnwiXBM0XYfuvBPvIURHBacfJUic=; __cfruid=046d655cbe145cd71cf6054c7f42408207c00c2e-1657824853; _cfuvid=tiCOoeOZkptAroVkL30vntaa4z77YekdNeBgapzRvGE-1657824853436-0-604800000',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    ]
    ordered_headers_list = []
    for headers in headers_list:
        h = OrderedDict()
    for header,value in headers.items():
        h[header]=value
        ordered_headers_list.append(h)
        tasks = []
    for itemId in ids:
        headers = random.choice(headers_list)
        tasks.append(asyncio.create_task(session.get(f"https://www.rewe.de/api/offer-details/{itemId}?searchTerm={itemId}", ssl=False, headers=headers)))
    return tasks

async def get_ids(ids):
    results = []
    print(len(ids))
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, ids)
        print(tasks)
        responses = await asyncio.gather(*tasks)
        print("AM I HERE YET?")
        
        for response in responses:
            print("working with id: {}".format(response))
            results.append(await response.json(content_type=None))
            n = 1
            offers = dict()
            for params in results:
                offers[n] = {
                    "name": params["product"]["description"],
                    "id": params["id"],
                    "price": params["pricing"]["priceInCent"],
                    "pastPrice": params["pricing"]["crossOutPriceInCent"],
                    "discount": params["pricing"]["advantage"],
                    "image": params["pictures"]["productImages"][0],
                    "validTill": params["validUntil"]
                }
                n += 1
    print(results)
    return offers

def offers(searchTerm: str) -> Dict:
    markets = _all_offers(searchTerm)
    complete = dict()
    i = 1
    ids = []
    for market in markets:
        ids_dups = []
        query = dict()
        query["id"] = markets[market]["id"]
        query["market"] = markets[market]["market"]
        m = 1
        start = len(ids)
        for category in markets[market]["offers"]:
            for offer in category["offers"]:
                if offer["id"] in ids:
                    if market != 1:
                        itemId = offer["id"]
                        ids_dups.append(itemId)
                else:
                    itemId = offer["id"]
                    ids.append(itemId)
        offers = asyncio.run(get_ids(ids[start:]))
        query["offers"] = offers
        complete[i] = query
        i += 1
        if market != len(markets):
            print("Sleeping now...")
            time.sleep(14)
            print("AWAKE!!")
    dict1 = complete
    out_file = open("offers.json", "w")
    
    json.dump(dict1, out_file, indent = 6)
    
    out_file.close()
    return complete
#1:34,84 total with .request() & Header & params
#1:30,33 total with .get()
#0:58,488 total with Session
#0:27 with async

offers("hoheluft")



