import requests
import json
import re


def get_uniport(ids: list):
    return requests.get("https://rest.uniprot.org/uniprotkb/accessions", params={'accessions': ids})


def get_ensembl(ids: list):
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    data = {"ids": ids}
    return requests.post("https://rest.ensembl.org/lookup/id", headers=headers, data=json.dumps(data))


def parse_response_uniprot(resp: dict):
    resp = resp.json()
    resp = resp["results"]
    info = {}

    for v in resp:
        acc = v['primaryAccession']
        species = v['organism']['scientificName']
        gene = v['genes']
        seq = v['sequence']
        info[acc] = {'organism': species, 'gene_info': gene, 'sequence_info': seq, 'type': 'protein'}

    return info

def parse_response_ensembl(resp: dict):
    resp = resp.json()
    info = {}

    for k, v in resp.items():
        sp = v['species']
        gene = v['id']
        canon = v['canonical_transcript']
        biotype = v['biotype']
        objectt = v['object_type']
        info[k] = {'organism': sp, 'gene_info': gene, 'canonical_transcript': canon, 'type': objectt, 'biotype': biotype}

    return info


def get_and_parse(ids: list):

    if re.fullmatch('ENS[A-Z]{1,6}\d{11}', ids[0]):
        resp = get_ensembl(ids)
        return parse_response_ensembl(resp)

    elif re.fullmatch('[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}', ids[0]):
        resp = get_uniport(ids)
        return parse_response_uniprot(resp)
    else:
        raise KeyError('Failed to find the request in any database')
