# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:28:23 2020

@author: Ryan
"""

import requests
import json


headers = {'authority': 'api.gartner.com',
           'method': 'GET',
           'path': '/search/gcom/channel/research?&filter=facetKi:%22Procurement%20and%20Strategic%20Sourcing%20Applications%22&q=&start=0&sort=dispDate+desc',
           'scheme': 'https',
           'accept': 'application/json, text/plain, */*',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'en-US,en;q=0.9,it;q=0.8',
           'cookie': '_gcl_au=1.1.1390245932.1605720300; __utma=256913437.1954659201.1605720300.1605720300.1605720300.1; __utmz=256913437.1605720300.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1954659201.1605720300; _hjid=8eb56d33-c380-4c8a-b841-0810aaf400fb; _gaexp=GAX1.2.63-3cUlZRo2g0i6DgPTFbA.18648.1!UBwhs4HjTPSahUbk67Tvsw.18649.0!wr89I4c8SdWvGM97n6GuXQ.18678.1!JncBa4beRLy63-ohrSlfGg.18681.1; optimizelyEndUserId=oeu1606098672291r0.03040023111321566; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%7D; NewGartnerHomepage=true; rxVisitor=16057202980976DOB5R03P461K8JRPGAJ15HT9J8S7NJ6; _gid=GA1.2.2107615612.1608519857; route-gnxtgen-notification=01bb58185715943d; route-gsearch-api=745513e704a8285b; route-guser=3a7bf5d47fdd9632; route-gpersonalization=a96fa131a86b3578; route-gfollow=5dd38ca70e7eb02b; route-gfeed=7c78b685ccc15dd0; route-glibrary=2772a6900cf29d97; route-gdocument=89898c32843bc3c3; GFEED=BD33CB93C1CBD02C3CD5EEC5E0D29690; WCW_Authentication=-5138929243468311817GUSPR100379940; WCW_Security=7912891258089273394SunDec20230159EST2020; WCW_Marker=2759491577; route-typeahead-api=d6e30b63525c15c6; GUSER=943D2BF3F257B6910B487926123E5BE9; GPRODSESSIONID=B862E8FAE3A2565419F64C5B57CEEDD7; GFOLLOW=8B9896C01C4447F4F96982CDE2F91D59; _gat_UA-8394889-3=1; GDOCUMENT=0194A1376AEF021BE1C68B1E8A7837A4; dtCookie=5$B21E45D13F6F9A851E060B93EE3B8F5F|74a9a024bfa90d62|1; dtSa=-; dtLatC=11; rxvt=1608530879490|1608527366914; dtPC=5$529079440_208h1vRQKOHURUGRKNFKGCLOWGCRVCCFFVUHJN-0e7',
           'dnt': '1',
           'origin': 'https://www.gartner.com',
           'referer': 'https://www.gartner.com/',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-site',
           'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

url = 'https://api.gartner.com/search/gcom/channel/research?&filter=facetKi:%22Procurement%20and%20Strategic%20Sourcing%20Applications%22&q=&start=10&sort=dispDate+desc'

with requests.session() as s:

    # load cookies:
    s.get('https://www.gartner.com/search/research?fc=facetKi:%22Procurement%20and%20Strategic%20Sourcing%20Applications%22&st=dispDate%20desc', headers=headers)

    # get data:
    data = s.get(url, headers=headers).json()

    # print data to screen:
    # print(json.dumps(data, indent=4))
