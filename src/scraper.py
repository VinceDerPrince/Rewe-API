import json
from typing import Dict, List
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
    tasks = []
    for itemId in ids:
        tasks.append(asyncio.create_task(session.get(f"https://www.rewe.de/api/offer-details/{itemId}?searchTerm={itemId}", ssl=False)))
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
            time.sleep(20)
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


