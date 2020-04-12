import requests
import re
import json


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


def _get_modality(init_dict, string):
    pos_modality = ["positive", "fusion", "mutation", "mutated", "deletion", "aberration",
                    "re arrangements", "alterations", "deleterious", "express", "overexpressing",
                    "rearrangements", "re-arrangements", "over-expressing", "over expressing"]
    neg_modality = ["wildtype", "negative", "wild-type", "neutral", "unknown"]
    for p in pos_modality:
        if re.search(pattern=r"\b" + re.escape(p) + r"\b", string=string, flags=re.IGNORECASE):
            init_dict["modality"] = "positive"
            init_dict["alteration_type"] = p
        else:
            for n in neg_modality:
                if re.search(pattern=r"\b" + re.escape(n) + r"\b", string=string, flags=re.IGNORECASE):
                    init_dict["modality"] = "negative"
                    init_dict["alteration_type"] = n
    return init_dict


def _get_additional_information(init_dict, string):
    if re.search(pattern=re.compile(r"^exon$"), string=string):
        if re.findall(re.compile(r"^exon\s\d+$"), string):
            exon = re.findall(re.compile(r"^exon\s\d+$"), string)[0]
        elif re.findall(re.compile(r"^\d+\sexon$"), string):
            exon = re.findall(re.compile(r"^\d+\sexon$"), string)[0]
        exon_type = int(re.findall(r"\d+", exon)[0])
        init_dict["exon"] = exon_type
    if re.findall(r"^[A-Z]{1}[0-9]{3}[A-Z]{1}$", string):
        init_dict["alteration"] = re.findall(r"^[A-Z]{1}[0-9]{3}[A-Z]{1}$", string)[0]
    return init_dict


def _use_hgnc_dict():
    with open('intermediate_hgnc_dict.json') as f:
        hgnc_dict = json.load(f)
    for key, value in hgnc_dict.items():
        init_list = []
        for v in value:
            init_list.append(re.sub(pattern=r'_', repl=' ', string=v))
        hgnc_dict[key] = init_list
    return hgnc_dict
