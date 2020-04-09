import re

from src.entity_extraction import _get_ees


def biomarker_object(r):
    pos_modality = ["positive", "fusion", "mutation", "mutated", "deletion", "aberration",
                    "re arrangements", "alterations", "deleterious", "express", "overexpressing",
                    "rearrangements", "re-arrangements", "over-expressing", "over expressing"]
    neg_modality = ["wildtype", "negative", "wild-type", "neutral", "unknown"]
    init_list = []
    for j in r:
        init_dict = {}
        for p in pos_modality:
            if re.search(pattern=r"\b" + re.escape(p) + r"\b", string=j, flags=re.IGNORECASE):
                init_dict["modality"] = "positive"
                init_dict["alteration_type"] = p
            else:
                for n in neg_modality:
                    if re.search(pattern=r"\b" + re.escape(n) + r"\b", string=j, flags=re.IGNORECASE):
                        init_dict["modality"] = "negative"
                        init_dict["alteration_type"] = n
        if init_dict:
            gene_tag = _get_ees(j)
            if gene_tag:
                init_dict["gene"] = gene_tag
        if "gene" in init_dict:
            if re.search(pattern=re.compile(r"^exon$"), string=j):
                if re.findall(re.compile(r"^exon\s\d+$"), j):
                    exon = re.findall(re.compile(r"^exon\s\d+$"), j)[0]
                elif re.findall(re.compile(r"^\d+\sexon$"), j):
                    exon = re.findall(re.compile(r"^\d+\sexon$"), j)[0]
                exon_type = int(re.findall(r"\d+", exon)[0])
                init_dict["exon"] = exon_type
            if re.findall(r"^[A-Z]{1}[0-9]{3}[A-Z]{1}$", j):
                init_dict["alteration"] = re.findall(r"^[A-Z]{1}[0-9]{3}[A-Z]{1}$", j)[0]
            init_list.append(init_dict)
    return init_list
