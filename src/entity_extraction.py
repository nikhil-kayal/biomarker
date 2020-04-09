import requests


def _get_ees(text):
    r = requests.post("http://n1-r20.w2v.servers.nferx.com/EntityExtraction/v3/getentities?sendData=1&subsume=type-wise&eesMode=0&whitelistTypes=",
                      data=('[{"text":"'+text+'"}]').encode(), headers={"Accept": "*/*",
                                                                        "Accept-Encoding": "gzip, deflate",
                                                                        "Authorization": "Basic bmZlcng6bmZlcngxMjM=",
                                                                        "Cache-Control": "no-cache",
                                                                        "Connection": "keep-alive",
                                                                        "Content-Length": "33",
                                                                        "Content-Type": "application/json",
                                                                        "Host": "n1-r20.w2v.servers.nferx.com",
                                                                        "Postman-Token": "e6909e2a-d79f-4371-b2df-4d580f8d9d4a,d62b7d4e-df2e-4453-b063-7bb757b9a19d",
                                                                        "User-Agent": "PostmanRuntime/7.18.0",
                                                                        "cache-control": "no-cache"},
                      cookies={"csrftoken": "ptcuMfzpmVOBNtff6p15ZkHnYY1ISgXg",
                               "sessionid": "sge9p7366t97d2nt9djbgoec15gude17"},
                      auth=('nferx', 'nferx123'))
    if 'result' not in r.json().keys():
        return {}
    if not r.json()['result'][0]['entities']:
        return {}
    if len(r.json()['result'][0]['entities']) > 0:
        if [d for d in r.json()['result'][0]['entities'] if d['entity_type'] == 'gene']:
            best_match = [d for d in r.json()['result'][0]['entities'] if d['entity_type'] == 'gene'][0]
            return best_match['normalized_phrase']