import json
from datetime import datetime, timedelta
from threading import Timer

import lxml.html
import pandas as pd
import requests
from flask_restplus import Namespace

api = Namespace('downloadLineagesInfo', description='downloadLineagesInfo')

########################################################################################################

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.61 Safari/537.36'
}

data_frame_lineage = []
data_frame_mutation = []


def load_lineages_and_mutation():
    def get_inner_text(inp):
        res = ''
        if inp.text:
            res += inp.text
        for x in inp:
            res += get_inner_text(x)
        return res.strip()

    with requests.Session() as s:
        url = 'https://cov-lineages.org/lineage_list.html'
        r = s.get(url, headers=headers)
        content = r.content
        tree = lxml.html.fromstring(content)
        table = tree.findall('.//table')[0]
        trs = table.findall('.//tr')
        data_frame_lineage.append(pd.DataFrame([[get_inner_text(x) for x in tr] for tr in trs[1:]],
                                               columns=[get_inner_text(x) for x in trs[0]]))
        # pd.DataFrame([[get_inner_text(x) for x in tr] for tr in trs[1:]],
        #             columns=[get_inner_text(x) for x in trs[0]]).to_csv("lineage_new.csv", index=False)

    with requests.Session() as s:
        try:
            url = 'https://www.ecdc.europa.eu/en/covid-19/variants-concern'
            r = s.get(url, headers=headers)
            content = r.content
            tree = lxml.html.fromstring(content)
            tables = tree.findall('.//table')
            for i, table in enumerate(tables):
                ths_head = table.findall('./thead/tr/th')
                columns = [get_inner_text(x) for x in ths_head]

                ths_body = table.findall('./tbody/tr')
                len(columns)
                rows = [[get_inner_text(x) for x in tr] for tr in ths_body]
                for r in rows:
                    if len(r) > len(columns):
                        del r[len(columns) - 1:len(r) - 1]
                data_frame_mutation.append(pd.DataFrame(rows, columns=columns))
                # print("qui2", dataFrameMutation)
                # pd.DataFrame(rows, columns=columns).to_csv(f"VC_{i}.csv", index=False)
        except:
            print("Something went wrong with ECDC table")

    x = datetime.today()
    y = x.replace(day=x.day, hour=1, minute=50, second=0, microsecond=0) + timedelta(days=1)
    delta_t = y - x
    secs = delta_t.total_seconds()
    t1 = Timer(secs, load_lineages_and_mutation)
    t1.start()


dict_lineage_mutation = {}


def create_dictionary():
    for table in data_frame_lineage:
        table2 = table.to_json(orient="records")
        table2 = json.loads(table2)
        for row in table2:
            single_line = {'lineage': row['Lineage']}
            description = row['Description'].replace(" ", "")
            if 'Aliasof' in description:
                start = 'Aliasof'
                end = ','
                single_line['alias'] = description[description.find(start) + len(start):description.find(end)]
            elif 'aliasof' in description:
                start = 'aliasof'
                end = ''
                single_line['alias'] = description[description.find(start) + len(start):description.rfind(end)]

            else:
                if row['Lineage'] == 'C.1.1':
                    single_line['alias'] = 'B.1.1.1.1.0'
                elif row['Lineage'] == 'C.10':
                    single_line['alias'] = 'B.1.1.1.10'
                elif row['Lineage'] == 'C.6':
                    single_line['alias'] = 'B.1.1.1.6'
                else:
                    single_line['alias'] = row['Lineage']

            single_line['WHO label'] = ''
            single_line['mutation'] = []
            single_line['additional_mutation'] = []
            dict_lineage_mutation[row['Lineage']] = single_line

    for table_mutation in data_frame_mutation:
        table_mutation2 = table_mutation.to_json(orient="records")
        table_mutation2 = json.loads(table_mutation2)
        for row in table_mutation2:
            if 'Lineage + additional mutations' in row:
                lineage = row['Lineage + additional mutations'].replace(' ', '')
                lineage = lineage.split('+')
                if len(lineage) > 1:
                    analyzed_lineage = lineage[0]
                    if analyzed_lineage in dict_lineage_mutation:
                        single_line = dict_lineage_mutation[analyzed_lineage]
                        additional_mutation = lineage[1]
                        additional_mutation = 'Spike_' + additional_mutation
                        single_line['additional_mutation'].append(additional_mutation)
                        dict_lineage_mutation[analyzed_lineage] = single_line
                else:
                    lineage = lineage[0]
                    arr_lineage = lineage.split('/')
                    for lin in arr_lineage:
                        if lin in dict_lineage_mutation:
                            single_line = dict_lineage_mutation[lin]
                            if dict_lineage_mutation[lin]['WHO label'] == '' and row['WHO label'] != 'n/a':
                                single_line['WHO label'] = row['WHO label']
                            mutation = row['Spike mutations of interest']
                            mutation = mutation.replace("'", "")
                            mutation = mutation.replace("ins", "-")
                            mutation = mutation.replace(' ', '').split(",")
                            arr_mut = []
                            for mut in mutation:
                                single_mutation = 'Spike_' + mut
                                arr_mut.append(single_mutation)
                            single_line['mutation'] = arr_mut
                            dict_lineage_mutation[lin] = single_line

    x = datetime.today()
    y = x.replace(day=x.day, hour=1, minute=55, second=0, microsecond=0) + timedelta(days=1)
    delta_t = y - x
    secs = delta_t.total_seconds()
    t2 = Timer(secs, create_dictionary)
    t2.start()


load_lineages_and_mutation()
create_dictionary()
