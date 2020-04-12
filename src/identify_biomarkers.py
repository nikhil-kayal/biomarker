import re

from src.utils import _get_ees, _get_modality, _get_additional_information, _use_hgnc_dict


def _get_biomarker_object_from_ees(r):
    """
    Function to identify bio-markers from entity extraction service
    :param r: List of sentences to identify biomarkers from
    :return: bio-marker object if modality & alteration type are present in the sentence
            [{"modality", "alteration_type", "gene", "exon", "alteration"}]
    """
    init_list = []
    for j in r:
        init_dict = {}
        init_dict = _get_modality(init_dict, j)
        if init_dict:
            gene_tag = _get_ees(j)
            if gene_tag:
                init_dict["gene"] = gene_tag
        if "gene" in init_dict:
            init_dict = _get_additional_information(init_dict, j)
            init_list.append(init_dict)
    return init_list


def _get_biomarker_object_from_hgnc_list(r):
    """
    Function to identify bio-markers from HGNC dictionary
    :param r: List of sentences to identify biomarkers from
    :return: bio-marker object if modality & alteration type are present in the sentence
            [{"modality", "alteration_type", "gene", "exon", "alteration"}]
    """
    hgnc_dict = _use_hgnc_dict()
    init_list = []
    for j in r:
        init_dict = {}
        init_dict = _get_modality(init_dict, j)
        if init_dict:
            for key, value in hgnc_dict.items():
                for v in value:
                    if re.search(pattern=r"\b" + re.escape(v) + r"\b", string=j, flags=re.IGNORECASE):
                        init_dict["gene"] = key
        if "gene" in init_dict:
            init_dict = _get_additional_information(init_dict, j)
            init_list.append(init_dict)
    return init_list

