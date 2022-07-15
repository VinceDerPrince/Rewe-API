import json
import random
from typing import Dict
from collections import OrderedDict
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

async def get_tasks(session, ids):
    headers_list = [
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540566%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; MRefererUrl=direct; c_lpv_a=1657825972768|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlYzMzMzI1N2YwY2RjNGI4MmM5NTU5YTIyOGNhMDFmODQyMGNjOGVkYzFkZGExN2Q3ZDkxZjgwYTlhNzI0NDU3N2E4ZDM4NWY0OTY2OWY2NjhiMzdkNzM1MjhhYjhiYTI3NDdkNTY4NjMwZGQ3NmFiMDM5Zjk0ZDA2YWE0ZjRjOTUwNDRhMTE5NTdhMjlkYmI0Y2FhZDczZGQwNzZhMzRjMzExMTY2ODk5OTQ1OTUwMzAwNDc2MGJmOWQ3M2VmMGQxZjE1ODBkNzllMGFkNmM1OGZjNDVkZmJhZDAyZDhmYTFjMjc3MzUyNDc5YTZkYjYzNGRmMzc3Yjk4ZjQ2MjRhZSIsImlhdCI6MTY1NzgyNTk5OSwiZXhwIjoxNjU3ODI2NTk5fQ.GI6LHTPn9nOgxd1mNmH9D3qG2HFXhvtGxTcGCEwHqykILZyQFpYr1dbyWmjrqIZlkHYo6rtwHP_MGVe3_O7o3A; __cf_bm=K8HVc1Tbh74V0DhUnLxiZjBzGe36yPCHuBv0Sqk5uOM-1657825999-0-AW0hO+kx2Acc+9LdMdJz7XojkL20vybv3bDTgaxQiqN61jEsz9mVAOSHedpQkjBKhwgHY70LkNmBejSfAy1z8pg=; __cfruid=a51c79dee470ff420df242cdc6a8c63dd9db17b9-1657825999; _cfuvid=V3LuSqENDR0XHraqP2LIhKCTPcJFD61YXGm9pJzdz4w-1657825999289-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540566%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; MRefererUrl=direct; c_lpv_a=1657825972768|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlYzMzMzI1N2YwY2RjNGI4MmM5NTU5YTIyOGNhMDFmODQyMGNjOGVkYzFkZGExN2Q3ZDkxZjgwYTlhNzI0NDU3N2E4ZDM4NWY0OTY2OWY2NjhiMzdkNzM1MjhhYjhiYTI3NDdkNTY4NjMwZGQ3NmFiMDM5Zjk0ZDA2YWE0ZjRjOTUwNDRhMTE5NTdhMjlkYmI0Y2FhZDczZGQwNzZhMzRjMzExMTY2ODk5OTQ1OTUwMzAwNDc2MGJmOWQ3M2VmMGQxZjE1ODBkNzllMGFkNmM1OGZjNDVkZmJhZDAyZDhmYTFjMjc3MzUyNDc5YTZkYjYzNGRmMzc3Yjk4ZjQ2MjRhZSIsImlhdCI6MTY1NzgyNTk5OSwiZXhwIjoxNjU3ODI2NTk5fQ.GI6LHTPn9nOgxd1mNmH9D3qG2HFXhvtGxTcGCEwHqykILZyQFpYr1dbyWmjrqIZlkHYo6rtwHP_MGVe3_O7o3A; __cf_bm=K8HVc1Tbh74V0DhUnLxiZjBzGe36yPCHuBv0Sqk5uOM-1657825999-0-AW0hO+kx2Acc+9LdMdJz7XojkL20vybv3bDTgaxQiqN61jEsz9mVAOSHedpQkjBKhwgHY70LkNmBejSfAy1z8pg=; __cfruid=a51c79dee470ff420df242cdc6a8c63dd9db17b9-1657825999; _cfuvid=V3LuSqENDR0XHraqP2LIhKCTPcJFD61YXGm9pJzdz4w-1657825999289-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540566%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; MRefererUrl=direct; c_lpv_a=1657825972768|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlYzMzMzI1N2YwY2RjNGI4MmM5NTU5YTIyOGNhMDFmODQyMGNjOGVkYzFkZGExN2Q3ZDkxZjgwYTlhNzI0NDU3N2E4ZDM4NWY0OTY2OWY2NjhiMzdkNzM1MjhhYjhiYTI3NDdkNTY4NjMwZGQ3NmFiMDM5Zjk0ZDA2YWE0ZjRjOTUwNDRhMTE5NTdhMjlkYmI0Y2FhZDczZGQwNzZhMzRjMzExMTY2ODk5OTQ1OTUwMzAwNDc2MGJmOWQ3M2VmMGQxZjE1ODBkNzllMGFkNmM1OGZjNDVkZmJhZDAyZDhmYTFjMjc3MzUyNDc5YTZkYjYzNGRmMzc3Yjk4ZjQ2MjRhZSIsImlhdCI6MTY1NzgyNTk5OSwiZXhwIjoxNjU3ODI2NTk5fQ.GI6LHTPn9nOgxd1mNmH9D3qG2HFXhvtGxTcGCEwHqykILZyQFpYr1dbyWmjrqIZlkHYo6rtwHP_MGVe3_O7o3A; __cf_bm=K8HVc1Tbh74V0DhUnLxiZjBzGe36yPCHuBv0Sqk5uOM-1657825999-0-AW0hO+kx2Acc+9LdMdJz7XojkL20vybv3bDTgaxQiqN61jEsz9mVAOSHedpQkjBKhwgHY70LkNmBejSfAy1z8pg=; __cfruid=a51c79dee470ff420df242cdc6a8c63dd9db17b9-1657825999; _cfuvid=V3LuSqENDR0XHraqP2LIhKCTPcJFD61YXGm9pJzdz4w-1657825999289-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) OPR/65.0.3467.48',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540566%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; MRefererUrl=direct; c_lpv_a=1657825972768|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlYzMzMzI1N2YwY2RjNGI4MmM5NTU5YTIyOGNhMDFmODQyMGNjOGVkYzFkZGExN2Q3ZDkxZjgwYTlhNzI0NDU3N2E4ZDM4NWY0OTY2OWY2NjhiMzdkNzM1MjhhYjhiYTI3NDdkNTY4NjMwZGQ3NmFiMDM5Zjk0ZDA2YWE0ZjRjOTUwNDRhMTE5NTdhMjlkYmI0Y2FhZDczZGQwNzZhMzRjMzExMTY2ODk5OTQ1OTUwMzAwNDc2MGJmOWQ3M2VmMGQxZjE1ODBkNzllMGFkNmM1OGZjNDVkZmJhZDAyZDhmYTFjMjc3MzUyNDc5YTZkYjYzNGRmMzc3Yjk4ZjQ2MjRhZSIsImlhdCI6MTY1NzgyNTk5OSwiZXhwIjoxNjU3ODI2NTk5fQ.GI6LHTPn9nOgxd1mNmH9D3qG2HFXhvtGxTcGCEwHqykILZyQFpYr1dbyWmjrqIZlkHYo6rtwHP_MGVe3_O7o3A; __cf_bm=K8HVc1Tbh74V0DhUnLxiZjBzGe36yPCHuBv0Sqk5uOM-1657825999-0-AW0hO+kx2Acc+9LdMdJz7XojkL20vybv3bDTgaxQiqN61jEsz9mVAOSHedpQkjBKhwgHY70LkNmBejSfAy1z8pg=; __cfruid=a51c79dee470ff420df242cdc6a8c63dd9db17b9-1657825999; _cfuvid=V3LuSqENDR0XHraqP2LIhKCTPcJFD61YXGm9pJzdz4w-1657825999289-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Edg/103.0.100.0',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540566%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; MRefererUrl=direct; c_lpv_a=1657825972768|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlYzMzMzI1N2YwY2RjNGI4MmM5NTU5YTIyOGNhMDFmODQyMGNjOGVkYzFkZGExN2Q3ZDkxZjgwYTlhNzI0NDU3N2E4ZDM4NWY0OTY2OWY2NjhiMzdkNzM1MjhhYjhiYTI3NDdkNTY4NjMwZGQ3NmFiMDM5Zjk0ZDA2YWE0ZjRjOTUwNDRhMTE5NTdhMjlkYmI0Y2FhZDczZGQwNzZhMzRjMzExMTY2ODk5OTQ1OTUwMzAwNDc2MGJmOWQ3M2VmMGQxZjE1ODBkNzllMGFkNmM1OGZjNDVkZmJhZDAyZDhmYTFjMjc3MzUyNDc5YTZkYjYzNGRmMzc3Yjk4ZjQ2MjRhZSIsImlhdCI6MTY1NzgyNTk5OSwiZXhwIjoxNjU3ODI2NTk5fQ.GI6LHTPn9nOgxd1mNmH9D3qG2HFXhvtGxTcGCEwHqykILZyQFpYr1dbyWmjrqIZlkHYo6rtwHP_MGVe3_O7o3A; __cf_bm=K8HVc1Tbh74V0DhUnLxiZjBzGe36yPCHuBv0Sqk5uOM-1657825999-0-AW0hO+kx2Acc+9LdMdJz7XojkL20vybv3bDTgaxQiqN61jEsz9mVAOSHedpQkjBKhwgHY70LkNmBejSfAy1z8pg=; __cfruid=a51c79dee470ff420df242cdc6a8c63dd9db17b9-1657825999; _cfuvid=V3LuSqENDR0XHraqP2LIhKCTPcJFD61YXGm9pJzdz4w-1657825999289-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/103.0.100.0',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540566%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; MRefererUrl=direct; c_lpv_a=1657825972768|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlYzMzMzI1N2YwY2RjNGI4MmM5NTU5YTIyOGNhMDFmODQyMGNjOGVkYzFkZGExN2Q3ZDkxZjgwYTlhNzI0NDU3N2E4ZDM4NWY0OTY2OWY2NjhiMzdkNzM1MjhhYjhiYTI3NDdkNTY4NjMwZGQ3NmFiMDM5Zjk0ZDA2YWE0ZjRjOTUwNDRhMTE5NTdhMjlkYmI0Y2FhZDczZGQwNzZhMzRjMzExMTY2ODk5OTQ1OTUwMzAwNDc2MGJmOWQ3M2VmMGQxZjE1ODBkNzllMGFkNmM1OGZjNDVkZmJhZDAyZDhmYTFjMjc3MzUyNDc5YTZkYjYzNGRmMzc3Yjk4ZjQ2MjRhZSIsImlhdCI6MTY1NzgyNTk5OSwiZXhwIjoxNjU3ODI2NTk5fQ.GI6LHTPn9nOgxd1mNmH9D3qG2HFXhvtGxTcGCEwHqykILZyQFpYr1dbyWmjrqIZlkHYo6rtwHP_MGVe3_O7o3A; __cf_bm=K8HVc1Tbh74V0DhUnLxiZjBzGe36yPCHuBv0Sqk5uOM-1657825999-0-AW0hO+kx2Acc+9LdMdJz7XojkL20vybv3bDTgaxQiqN61jEsz9mVAOSHedpQkjBKhwgHY70LkNmBejSfAy1z8pg=; __cfruid=a51c79dee470ff420df242cdc6a8c63dd9db17b9-1657825999; _cfuvid=V3LuSqENDR0XHraqP2LIhKCTPcJFD61YXGm9pJzdz4w-1657825999289-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540566%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; MRefererUrl=direct; c_lpv_a=1657825972768|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlYzMzMzI1N2YwY2RjNGI4MmM5NTU5YTIyOGNhMDFmODQyMGNjOGVkYzFkZGExN2Q3ZDkxZjgwYTlhNzI0NDU3N2E4ZDM4NWY0OTY2OWY2NjhiMzdkNzM1MjhhYjhiYTI3NDdkNTY4NjMwZGQ3NmFiMDM5Zjk0ZDA2YWE0ZjRjOTUwNDRhMTE5NTdhMjlkYmI0Y2FhZDczZGQwNzZhMzRjMzExMTY2ODk5OTQ1OTUwMzAwNDc2MGJmOWQ3M2VmMGQxZjE1ODBkNzllMGFkNmM1OGZjNDVkZmJhZDAyZDhmYTFjMjc3MzUyNDc5YTZkYjYzNGRmMzc3Yjk4ZjQ2MjRhZSIsImlhdCI6MTY1NzgyNTk5OSwiZXhwIjoxNjU3ODI2NTk5fQ.GI6LHTPn9nOgxd1mNmH9D3qG2HFXhvtGxTcGCEwHqykILZyQFpYr1dbyWmjrqIZlkHYo6rtwHP_MGVe3_O7o3A; __cf_bm=K8HVc1Tbh74V0DhUnLxiZjBzGe36yPCHuBv0Sqk5uOM-1657825999-0-AW0hO+kx2Acc+9LdMdJz7XojkL20vybv3bDTgaxQiqN61jEsz9mVAOSHedpQkjBKhwgHY70LkNmBejSfAy1z8pg=; __cfruid=a51c79dee470ff420df242cdc6a8c63dd9db17b9-1657825999; _cfuvid=V3LuSqENDR0XHraqP2LIhKCTPcJFD61YXGm9pJzdz4w-1657825999289-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540566%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; MRefererUrl=direct; c_lpv_a=1657825972768|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlYzMzMzI1N2YwY2RjNGI4MmM5NTU5YTIyOGNhMDFmODQyMGNjOGVkYzFkZGExN2Q3ZDkxZjgwYTlhNzI0NDU3N2E4ZDM4NWY0OTY2OWY2NjhiMzdkNzM1MjhhYjhiYTI3NDdkNTY4NjMwZGQ3NmFiMDM5Zjk0ZDA2YWE0ZjRjOTUwNDRhMTE5NTdhMjlkYmI0Y2FhZDczZGQwNzZhMzRjMzExMTY2ODk5OTQ1OTUwMzAwNDc2MGJmOWQ3M2VmMGQxZjE1ODBkNzllMGFkNmM1OGZjNDVkZmJhZDAyZDhmYTFjMjc3MzUyNDc5YTZkYjYzNGRmMzc3Yjk4ZjQ2MjRhZSIsImlhdCI6MTY1NzgyNTk5OSwiZXhwIjoxNjU3ODI2NTk5fQ.GI6LHTPn9nOgxd1mNmH9D3qG2HFXhvtGxTcGCEwHqykILZyQFpYr1dbyWmjrqIZlkHYo6rtwHP_MGVe3_O7o3A; __cf_bm=K8HVc1Tbh74V0DhUnLxiZjBzGe36yPCHuBv0Sqk5uOM-1657825999-0-AW0hO+kx2Acc+9LdMdJz7XojkL20vybv3bDTgaxQiqN61jEsz9mVAOSHedpQkjBKhwgHY70LkNmBejSfAy1z8pg=; __cfruid=a51c79dee470ff420df242cdc6a8c63dd9db17b9-1657825999; _cfuvid=V3LuSqENDR0XHraqP2LIhKCTPcJFD61YXGm9pJzdz4w-1657825999289-0-604800000',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Alt-Used': 'www.rewe.de',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'mtc=s%3AIBreifMtpUrWAdmOZcFokQgyKHN3aXRjaC1ydWxlLWluc2lnaHRzOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyIHBheWJhY2stZXZvdWNoZXIkdHJiby1iYW5uZXItZGVsbW9kJnBheWJhY2stZWNvdXBvbi1hcGlAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2VEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlciptb2JpbGUtcGF5YmFjay1hcGlLZXkmcGF5YmFjay1jYXJkLWNoYW5nZSRtZW5nZW5yYWJhdHRpZXJ1bmcocHJvZHVjdGxpc3QtY2l0cnVzYWQ%2BcHJvZHVjdGxpc3QtbmF2aWdhdGlvbi10cmFja2luZzZpbmktMzgxMi1oaWRlLXJlZ3VsYXItcHJpY2UmbWFya3RzZWl0ZS1yZWxvYWRlZF5wcm9kdWN0bGlzdC1mdW5uZWxpbmctemVyby1yZXN1bHRzLXBhcmNlbC1jaGVjayh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4qYWJob2xzZXJ2aWNlLXJlbG9hZGVkKHBheWJhY2stdm91Y2hlci13YWxsLG9mZmVyLWRldGFpbHMtdHJhY2tpbmcUbmV3LWhlYWRlcjpwYXliYWNrLXRhcmdldGVkLWJvbnVzLWNvdXBvbjRwcm9kdWN0bGlzdC1uZXctZGVhbHMtcGFnZS5uZXctbmF2aWdhdGlvbi10cmFja2luZy5wYXliYWNrLXJld2UtbmV3c2xldHRlcgAAAA%3D%3D.aMPY%2Fn25vPQ%2B%2BlKg0HKRWRgXm%2FsuGagj2EexlYA7mbs; MRefererUrl=direct; _rdfa=s%3A4882f577-c3b9-4409-ad69-c4e2172370ff.PfateuO%2BVfzNpXkpkhQJLIvOLSpnlg0hvVgLLM52JHk; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJiNTQ5ZWJmZWNjZDcxYjczZTk0YjgwOTE0N2UwNDc1MWNmYTM5NTQ2MDkwZGEyZWJjMjNmYzZhYjQxYzg3YjlmOTY5N2NhNDkyY2UzNjU5Njk0MTMwNDM0ODU4YmViMWQ2ODgzNGQzMzJlMDc2NGQ2OGY3Y2U5ZTcxZGU0YjE5MTBkZDM5ZTIwN2QyYWM1ZWI5NmI4YTE0OTI4OTEyOWFkOWMzZWM5YjU1ZGI2YWNkMmI1MjI0NTZlNGVlZTE4YTcyNzRkMTQ4NWNkNjczNmQxNzBmOWNmMWIwYTg2ZGZhMjE1NDk3NmE4NTVmNGM3ZGU5NzgwNGZjMWNiYmFlNDliIiwiaWF0IjoxNjU3ODY2NzMyLCJleHAiOjE2NTc4NjczMzJ9.B68ePFqaM0WNiNcjc8gc8ivv7ygZxpKe1lQAmW8gYRe0oPgAWc7lKTk0mv1eOoHm70Bq05-pLQB0RtSitbfvKw; __cf_bm=vinTAxUzWJNMKpnqXtbY54h4vPgm4uABSS7HLGq470o-1657866732-0-AZoDxk0cqeUtR/2xQxnw1gv4L2UtEKLSWz46q9YSiIJdJAa0jjvlRSwN0BAPF+2Tu5kpy/eIPI5vgOOv1StDz1Q=; __cfruid=542cb208463df7610b34f4501837cfeaf01273e9-1657866732; _cfuvid=vzyZ9EhoUxeAamOqDEJb2_mbGUORkycRB0K_KK.ensI-1657866732676-0-604800000',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    },
    {
        'authority': 'www.rewe.de',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'mtc=s%3AIFveEZmUgXYhLMioPWZucGI0IHBheWJhY2stZXZvdWNoZXIoc3dpdGNoLXJ1bGUtaW5zaWdodHNEcHJvZHVjdGxpc3QtbW9iaWxlLWNhdGVnb3J5LWZpbHRlchRuZXctaGVhZGVyOnBheWJhY2stdGFyZ2V0ZWQtYm9udXMtY291cG9uNmluaS0zODEyLWhpZGUtcmVndWxhci1wcmljZT5wcm9kdWN0bGlzdC1uYXZpZ2F0aW9uLXRyYWNraW5nKm1vYmlsZS1wYXliYWNrLWFwaUtleSh3b29raWVlcy1waWNrdXAtcGFnZSpwYXliYWNrLXRhcmdldGVkLWJ1cm4ocHJvZHVjdGxpc3QtY2l0cnVzYWQubmV3LW5hdmlnYXRpb24tdHJhY2tpbmdAaW5pLTM2NzgtZGlzbWFudGxpbmctbWFya2V0cGxhY2UocGF5YmFjay12b3VjaGVyLXdhbGw4cHJvZHVjdGxpc3QtdGVzdGluZy1jaXRydXNhZCxvZmZlci1kZXRhaWxzLXRyYWNraW5nOnByb2R1Y3RsaXN0LW5ldy1tb2JpbGUtZmlsdGVyJnBheWJhY2stY2FyZC1jaGFuZ2U2cHJvZHVjdGxpc3QtY2F0ZWdvcnktdGVhc2VyXnByb2R1Y3RsaXN0LWZ1bm5lbGluZy16ZXJvLXJlc3VsdHMtcGFyY2VsLWNoZWNrNHByb2R1Y3RsaXN0LW5ldy1kZWFscy1wYWdlJG1lbmdlbnJhYmF0dGllcnVuZyZwYXliYWNrLWVjb3Vwb24tYXBpLnBheWJhY2stcmV3ZS1uZXdzbGV0dGVyKmFiaG9sc2VydmljZS1yZWxvYWRlZCZtYXJrdHNlaXRlLXJlbG9hZGVkAAAA.pTjGHo8PyEZIf7d2bvAKjiTwVEoyZEmrEKzjV1ZJTKk; _rdfa=s%3A9730915a-816b-429d-9652-1d077a2a325f.%2FWshR2kf2x9M8ME%2By8kYxd%2Bxa3PDm1%2F4IGVt0Qjpo1Y; consentSettings={%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22advertisingOnsite%22:1%2C%22marketingOnsite%22:1%2C%22basicAnalytics%22:1%2C%22sessionMonitoring%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22extendedAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22targetGroup%22:0%2C%22userProfiling%22:0%2C%22crossDomainAnalytics%22:0%2C%22status%22:0}; icVarSave=tc105_c; s_ecid=MCMID%7C91568549989751941101916660413445705603; AMCVS_65BE20B35350E8DE0A490D45%40AdobeOrg=1; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=-1124106680%7CMCMID%7C91568549989751941101916660413445705603%7CMCAID%7CNONE%7CMCOPTOUT-1657295754s%7CNONE%7CvVersion%7C5.2.0; MRefererUrl=direct; __cfruid=ceb97abfb70d5ac5410709eb3a54487e65e4428c-1657827732; _cfuvid=vtZiSxuoquQWUMn11ygM4aO.PZHySBBrtOY1.5uvn.g-1657827732073-0-604800000; marketsCookie=%7B%22online%22%3A%7B%7D%2C%22stationary%22%3A%7B%22wwIdent%22%3A%22540319%22%2C%22marketZipCode%22%3A%2220253%22%2C%22serviceTypes%22%3A%5B%22STATIONARY%22%5D%7D%7D; c_lpv_a=1657827851267|dir_direct_nn_nn_nn_nn_nn_nn_nn; rstp=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJhZWIwNzI1MWU3MTY0OTQ1ZDdmNDU2NDZmNzUwMDMxNjZjZmU3MDhlMGY5NTU1YTk5NjNhZWM2ODBlMGQxMWE3MTdiYWQyZDQ5Mzg4MGI3ZTc2NzgzYjY0YmU2ZmE3ZTg3OTRmZThhNzIzYWEzN2VhYjI1NTE0ZGY1Y2MzYmZjODM2NjY1OTI1Y2E4YjY5MzNiNDcyOGQ3ZGE1Mjc4MWFlNGE3ZGExZDEzYTk2YzFmOWNhMDc5OGVlMTMyOGY1MGU2MTk0NDI4YTdhZjAyYTBhNTdlMWM1ZDhmN2VkNWJiZTJkOWFlYmMxMWU3NGEyNWEyMzQ3ZWMxMTRlYjk1ZmM5NTZkZTIzMWY1MDNmZjIzNjBmYzgxN2I4YzVmYjZjODY3ZjhhMmVmMTc3OWJhMWM5ODY1MzRlOGEzZmM0OThmYTUxMTg2NmZlYTJmMjMyODMxMjNhZjUyM2UxNThkZDVjYWJhNDdmY2EzYzRkZGZhMzkxMTM1NTdmNTA2ZTEwYmUwY2NhN2M4ZWI3NmIzNDNlNjc0NGE4MjI0NDA3MGY5OCIsImlhdCI6MTY1NzgyODY3OSwiZXhwIjoxNjU3ODI5Mjc5fQ.QHrcKalQgwAk0aZxp6Y4qxN31Ilr96faiWarEsrV-KwCM-gYtQtWMUYQYV18VjZLFmpEXOwM8gzy2OQABe71pg',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.100.0',
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
        headers = random.choice(ordered_headers_list)
        tasks.append(asyncio.create_task(session.get(f"https://www.rewe.de/api/offer-details/{itemId}?searchTerm={itemId}", ssl=False, headers=headers)))
    return await tasks

async def get_ids(ids):
    results = []
    print(len(ids))
    async with aiohttp.ClientSession() as session:
        tasks = await get_tasks(session, ids)
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
    dict1 = complete
    out_file = open("offers.json", "w")
    
    json.dump(dict1, out_file, indent = 6)
    
    out_file.close()
    return complete
#1:34,84 total with .request() & Header & params
#1:30,33 total with .get()
#0:58,488 total with Session
#0:27 with async
#0:11,694 as of right now: concurrent
