from __future__ import print_function
import sys
import os
import json
from collections import defaultdict
from xml.etree import ElementTree as ET
from pykakasi import kakasi

KAKASI = kakasi()
KAKASI.setMode('K', 'H')
KAKASI.setMode('J', 'H')
JA_CONV = KAKASI.getConverter()


def process_files(files):
    data = defaultdict(dict)
    for f in files:
        basename = os.path.basename(f)
        lang, _ = os.path.splitext(basename)
        for zone, city in process_file(f).items():
            data[zone][lang] = city
    return data


def process_file(in_file):
    xml = ET.parse(in_file)
    result = {}
    for zone in xml.findall('.//zone'):
        name = zone.get('type')
        city_elem = zone.find('.//exemplarCity')
        if city_elem is not None:
            city = city_elem.text
            result[name] = city
    return result


def pivot_langs(data):
    result = defaultdict(dict)
    for zone, translations in data.items():
        try:
            en = translations['en']
        except KeyError:
            en = zone.split('/')[-1].replace('_', ' ')
        for lang, translation in translations.items():
            trans_norm = translation.lower()
            result[trans_norm] = en
            if lang == 'ja':
                try:
                    ja = JA_CONV.do(trans_norm)
                    result[ja] = en
                except KeyError:
                    pass
    return result


def print_tsv(data):
    langs = set(lang for translations in data.values()
                for lang in translations)
    sorted_langs = list(sorted(langs))
    print('Time Zone', *sorted_langs, sep='\t')
    for zone, translations in data.items():
        all_trans = [translations.get(lang, '') for lang in sorted_langs]
        print(zone, *all_trans, sep='\t')


def main():
    args = sys.argv[1:]
    data = process_files(args[1:])
    if args[0] == 'json':
        pivoted = pivot_langs(data)
        json.dump(pivoted, sys.stdout)
    elif args[0] == 'tsv':
        print_tsv(data)


if __name__ == '__main__':
    main()
