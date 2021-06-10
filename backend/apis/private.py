from __future__ import print_function
# %config Completer.use_jedi = False
import datetime
import os
import re

import requests
import io
import http.client
import json

import pandas as pd
from collections import defaultdict
from Bio import SeqIO
from io import StringIO
from Bio import Align, Seq, pairwise2
from Bio.Data import CodonTable
import numpy as np
import itertools
import collections
import logomaker
import tqdm
import psycopg2
import matplotlib.pyplot as plt

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.core.display import HTML

from flask_restplus import Namespace, Resource


api = Namespace('private', description='private')


session_parser = api.parser()
session_parser.add_argument('session_id', type=str)


session_ids = []

dict_session_files = {}

########################################################################################################


@api.route('/upload_csv')
class FieldList(Resource):
    @api.doc('upload_csv')
    def post(self):
        key_generated = False
        session_id = ""
        while not key_generated:
            session_id = os.urandom(12).hex()
            if session_id not in session_ids:
                session_ids.append(session_id)
                key_generated = True

        payload = api.payload
        file_csv = payload.get('fileCSV')

        metadata = defaultdict(dict)
        file_csv = io.StringIO(file_csv)
        file_csv.readline()

        for line in file_csv:
            s = line.strip().split(",")
            cluster = s[0]
            seq_id = s[1]
            data = s[2]
            label = s[4]
            value = s[5]

            metadata[seq_id]['cluster'] = cluster
            metadata[seq_id]["date"] = data
            metadata[seq_id][label] = value

        dict_session_files[session_id] = {}
        dict_session_files[session_id]['metadata'] = metadata

        return session_id


@api.route('/upload_fasta')
class FieldList(Resource):
    @api.doc('upload_fasta', params={'session_id': ''})
    def post(self):
        payload = api.payload
        file_fasta = payload.get('fileFASTA')

        args = session_parser.parse_args()
        session_id = args['session_id']

        fasta_io = StringIO(file_fasta)

        fasta_sequences = SeqIO.parse(fasta_io, "fasta")
        l_fasta = list(fasta_sequences)

        dict_session_files[session_id]['fasta'] = l_fasta

        # reference = str(SeqIO.parse('ref_cov2.fasta', 'fasta').__next__().seq).lower()

        spike_start, spike_stop, spike_aa = 21563, 25384, "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRARSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCLKGCCSCGSCCKFDEDDSEPVLKGVKLHYT"

        table = CodonTable.ambiguous_dna_by_id[1]
        conversion_table = table.__dict__['forward_table'].__dict__['forward_table']
        conversion_table['TAA'] = "*"
        conversion_table['TGA'] = "*"
        conversion_table['TAG'] = "*"

        nuc = set(['A', 'C', 'G', 'T'])

        def n2aa(codon):
            if 'N' in codon:
                return 'X'
            elif '-' in codon:
                return "#"
            elif len(set(codon).difference(nuc)) > 0:
                return "X"
            else:
                return conversion_table[codon]

        def nseq2aaseq(seq):
            iseq = seq.replace("---", "")
            i = 0
            aaseq = ""
            while i < len(iseq):
                aaseq += n2aa(iseq[i:i + 3])
                i += 3

            return aaseq

        table = CodonTable.ambiguous_dna_by_id[1]

        mut_dataset = []
        seqs_1_epi = []
        seqs_2_epi = []

        for s in tqdm.tqdm(l_fasta):
            aa_spike = nseq2aaseq(str(s.seq[spike_start - 1:spike_stop]))
            alignment_aa = pairwise2.align.globalms(spike_aa, aa_spike, 3, -1, -3, -1)
            l_mut = []

            seqs_1_epi.append(alignment_aa[0].seqB[1185 - 1:1202])
            seqs_2_epi.append(alignment_aa[0].seqB[16:24])

            for i, r, s in zip(range(1, len(alignment_aa[0].seqA) + 1), alignment_aa[0].seqA, alignment_aa[0].seqB):
                if r != s and s != "X":
                    l_mut.append((i, r, s))
            mut_dataset.append(l_mut)

        mut_dict2 = [{'id': i,
                     "mut": mut,
                     "fs_flag": len([x for x in mut if x[2] == '#']) > 0
                     } for i, mut in zip([x.id for x in l_fasta], mut_dataset)]

        dict_session_files[session_id]['mut_dict'] = mut_dict2

        return mut_dict2


@api.route('/fields')
class FieldList(Resource):
    @api.doc('get_field_list', params={'session_id': ''})
    def get(self):
        args = session_parser.parse_args()
        session_id = args['session_id']

        metadata = dict_session_files[session_id]['metadata']

        all_metadata_list = []

        line = list(metadata.items())[0]
        for key, value in line[1].items():
            if key not in all_metadata_list:
                all_metadata_list.append(key)

        return all_metadata_list


@api.route('/sequence')
class FieldList(Resource):
    @api.doc('get_sequence_metadata', params={'session_id': ''})
    def post(self):
        payload = api.payload
        sequence_id = payload.get('sequence_id')

        args = session_parser.parse_args()
        session_id = args['session_id']

        metadata = dict_session_files[session_id]['metadata']

        sequence_metadata = metadata[sequence_id]

        return sequence_metadata


@api.route('/field/<field_name>')
class FieldList(Resource):
    @api.doc('get_specific_field_count', params={'session_id': ''})
    def post(self, field_name):
        payload = api.payload
        selected_filters = payload.get('selectedFilters')

        args = session_parser.parse_args()
        session_id = args['session_id']

        metadata = dict_session_files[session_id]['metadata']

        if selected_filters is not None:
            metadata = filter_metadata(metadata, selected_filters)

        specific_metadata = []

        for line in metadata.items():
            for key, value in line[1].items():
                if key == field_name:
                    found = False
                    for item in specific_metadata:
                        if value == item['name']:
                            item['value'] = item['value'] + 1
                            found = True
                    if not found:
                        specific_metadata.append({'name': value, 'value': 1})

        return specific_metadata


@api.route('/query')
class FieldList(Resource):
    @api.doc('query', params={'session_id': ''})
    def post(self):
        payload = api.payload
        selected_filters = payload.get('selectedFilters')

        args = session_parser.parse_args()
        session_id = args['session_id']

        mut_dict = dict_session_files[session_id]['mut_dict']

        for item in mut_dict:
            all_mut = item['mut']
            list_mut = []
            for mut in all_mut:
                list_mut.append(tuple(mut))
            item['mut'] = list_mut

        spike_start, spike_stop, spike_aa = 21563, 25384, "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRARSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCLKGCCSCGSCCKFDEDDSEPVLKGVKLHYT"

        protein = 'Spike (surface glycoprotein)'

        metadata = dict_session_files[session_id]['metadata']

        if selected_filters is not None:
            metadata = filter_metadata(metadata, selected_filters)

        metadata = pd.DataFrame(metadata).T

        metadata['mut'] = pd.DataFrame(mut_dict).set_index('id').mut

        metadata['fs_flag'] = pd.DataFrame(mut_dict).set_index('id').fs_flag

        list_pairs = sorted(list(
           set([tuple(x) for x in metadata[['cluster', 'lineage']].values])))

        mut_stats = {}
        for c, l in list_pairs:
            rows_m = metadata[(metadata['cluster'] == c) & (metadata['lineage'] == l)]
            samples = rows_m.shape[0]

            mut = list(rows_m['mut'].values)
            mut_counts = collections.Counter([item for sublist in mut for item in sublist])

            mut_stats[(c, l)] = (samples, mut_counts)

        conn = http.client.HTTPConnection('geco.deib.polimi.it')

        conn.request('GET', '/virusurf_epitope/api/epitope/statisticsMutationsLineagesGET')

        response = conn.getresponse()
        lineage_stats = response.read().decode()

        lineage_stats = json.loads(lineage_stats)

        list_data_mut_table = []
        for (c, l), (n, cnt) in list(mut_stats.items()):
            for m in cnt.keys():
                l1 = str(l)
                m1 = str(m)
                if l not in lineage_stats:
                    lineage_stats[l1] = {}
                m2 = m1.replace(")", f", '{protein}')")
                cnt_c = cnt[m]
                frq_l = lineage_stats[l1].get(m2, -1)
                frq_c = cnt_c / n
                if frq_l != -1:
                    fc = frq_c / (frq_l + 0.000001)
                else:
                    fc = -1

                list_data_mut_table.append((c, l, m, cnt_c, frq_l, frq_c, fc))

        mut_table = pd.DataFrame(list_data_mut_table, columns=["cluster",
                                                               "lineage",
                                                               'mutation',
                                                               "# cluster",
                                                               "% lineage",
                                                               "% cluster",
                                                               "FC"])

        conn = http.client.HTTPConnection('geco.deib.polimi.it')

        conn.request('GET', '/virusurf_epitope/api/epitope/allEpitopes')

        response_epi = conn.getresponse()
        epitopes = response_epi.read().decode()

        epitopes = json.loads(epitopes)

        epitopes = pd.DataFrame.from_dict(epitopes, orient='columns')

        def enrich_mutations(m):
            selected_epitopes = epitopes[
                (epitopes['epi_frag_annotation_start'] <= m[0]) & (epitopes['epi_frag_annotation_stop'] >= m[0])]
            selected_linear = selected_epitopes[selected_epitopes.is_linear]
            selected_nonlin = selected_epitopes[~selected_epitopes.is_linear]
            s_min = selected_linear.epi_annotation_start.min()
            s_max = selected_linear.epi_annotation_stop.max()
            epi_seq = spike_aa[s_min - 1:s_max]
            publications_linear = list(set(list(itertools.chain(*list(selected_linear.pubs)))))
            publications_nonlin = list(set(list(itertools.chain(*list(selected_nonlin.pubs)))))

            return (s_min,
                    s_max,
                    epi_seq,
                    selected_linear.shape[0],
                    selected_nonlin.shape[0],
                    publications_linear,
                    publications_nonlin,
                    len(publications_linear),
                    len(publications_nonlin))

        mut_table[["epi_start", "epi_stop", "epi_seq", "#linear", "#non-linear", "pubs linear", "pubs non-linear",
                   "#pubs linear", "#pubs non-linear"]] = pd.DataFrame(
            mut_table.mutation.apply(enrich_mutations).tolist(), index=mut_table.index)

        def create_filter(m):
            return lambda x: m in x

        def find_sequences(x):
            c = x.cluster
            m = x.mutation
            l = x.lineage
            return list(metadata[metadata.mut.apply(create_filter(m)) & (metadata.cluster == c) & (
                    metadata.lineage == l)].index)

        mut_table['sequences'] = mut_table.apply(find_sequences, axis=1)

        # annotations = pd.read_csv("/Users/LucaCillo/Desktop/UFL project/backend/apis/spike_annotations.tsv", delimiter='\t')

        annotations = pd.read_csv("apis/protein_annotations.csv",
                                  delimiter=',')

        def find_annotation(m):
            # return list(annotations[(annotations.Start <= m[0]) & (annotations.Stop >= m[0])].Annotation)
            ann = annotations[(annotations.Protein == protein) & (annotations.Begin <= m[0]) & (annotations.End >= m[0])]
            ann2 = ann[['Type', 'Category', 'Description', 'EvidenceUrls']]
            ann3 = ann2.to_json(orient="records")
            return json.loads(ann3)

        mut_table['annotations'] = mut_table.mutation.apply(find_annotation)

        res = mut_table

        list_dict = []
        for index, row in list(res.iterrows()):
            list_dict.append(dict(row))

        array_cluster = []
        array_lineage = []
        statistics_cluster = {}
        statistics_lineage = {}
        statistics_lineage_mut = {}
        statistics_cluster_mut = {}

        array_cluster_lineage = []
        statistics_group_lineage = {}
        statistics_group_lineage_mut = {}
        statistics_group_count_mut_seq = {}

        for item in list_dict:
            comb = [item['cluster'], item['lineage']]
            cl = item['cluster']
            lin = item['lineage']
            combo = cl + '-' + lin
            if comb not in array_cluster_lineage:
                cl = item['cluster']
                lin = item['lineage']
                comb2 = [cl, lin]
                array_cluster_lineage.append(comb2)
                combo = cl + '-' + lin
                statistics_group_lineage[f'{combo}'] = item['sequences'].copy()
                statistics_group_lineage_mut[f'{combo}'] = [
                    str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2])]
                mutat = str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2])

                single_mut = []
                statistics_group_count_mut_seq[f'{combo}'] = single_mut
                for seq in item['sequences']:
                    single_mut = {'seq': seq, 'count': [mutat]}
                    statistics_group_count_mut_seq[f'{combo}'].append(single_mut)

            else:
                statistics_group_lineage_mut[f'{combo}'].append(
                    str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2]))
                mutat = str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2])
                for seq in item['sequences']:
                    cl = item['cluster']
                    lin = item['lineage']
                    combo = cl + '-' + lin
                    if seq not in statistics_group_lineage[f'{combo}']:
                        statistics_group_lineage[f'{combo}'].append(seq)
                    if not any(d['seq'] == seq for d in statistics_group_count_mut_seq[f'{combo}']):
                        single_mut = {'seq': seq, 'count': [mutat]}
                        statistics_group_count_mut_seq[f'{combo}'].append(single_mut)
                    else:
                        for d in statistics_group_count_mut_seq[f'{combo}']:
                            if d['seq'] == seq:
                                d['count'].append(mutat)
            if item['cluster'] not in array_cluster:
                cl = item['cluster']
                array_cluster.append(cl)
                statistics_cluster[f'{cl}'] = item['sequences'].copy()
                statistics_cluster_mut[f'{cl}'] = [
                    str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2])]
            else:
                stri = str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2])
                if stri not in statistics_cluster_mut[f'{cl}']:
                    statistics_cluster_mut[f'{cl}'].append(
                        str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2]))
                for seq in item['sequences']:
                    if seq not in statistics_cluster[item['cluster']]:
                        cl = item['cluster']
                        statistics_cluster[f'{cl}'].append(seq)
            if item['lineage'] not in array_lineage:
                lin = item['lineage']
                array_lineage.append(lin)
                statistics_lineage[f'{lin}'] = item['sequences'].copy()
                statistics_lineage_mut[f'{lin}'] = [
                    str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2])]
            else:
                stri = str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2])
                if stri not in statistics_lineage_mut[f'{lin}']:
                    statistics_lineage_mut[f'{lin}'].append(
                        str(item['mutation'][0]) + '|' + str(item['mutation'][1]) + '|' + str(item['mutation'][2]))
                for seq in item['sequences']:
                    if seq not in statistics_lineage[item['lineage']]:
                        lin = item['lineage']
                        statistics_lineage[f'{lin}'].append(seq)


        # seq_mut_arr = []
        # y = 0
        # for seq in mut_dict:
        #     seq_json = {}
        #     meta = metadata2[seq['id']]
        #     if len(meta) != 0:
        #         y = y + 1
        #         print("", y)
        #         lineage = meta['lineage']
        #         mutations = seq['mut']
        #         strstr = seq['id'].split('|')
        #         conn = http.client.HTTPConnection('geco.deib.polimi.it')
        #         headers = {'Content-type': 'application/json'}
        #         foo = strstr[1]
        #         json_data = json.dumps(foo)
        #         conn.request('POST', '/virusurf_epitope/api/epitope/mutationForSequence', json_data, headers)
        #         response = conn.getresponse()
        #         all_res = response.read().decode()
        #         all_res2 = json.loads(all_res)
        #         seq_json['id_loaded'] = seq['id']
        #         seq_json['id_gisaid'] = strstr[1]
        #         seq_json['lineage_loaded'] = lineage
        #         if not all_res2:
        #             seq_json['lineage_gisaid'] = ""
        #         else:
        #             seq_json['lineage_gisaid'] = all_res2[0]['lineage']
        #         if seq_json['lineage_loaded'] == seq_json['lineage_gisaid']:
        #             seq_json['same_lineage'] = True
        #         else:
        #             seq_json['same_lineage'] = False
        #
        #         arr_mutation_loaded = []
        #         if not all_res2:
        #             arr_mutation_gisaid = []
        #             seq_json['num_mut_gisaid'] = len(arr_mutation_gisaid)
        #         else:
        #             string_mut = all_res2[0]['array_agg']
        #             string_mut = string_mut[2:]
        #             string_mut = string_mut[:-2]
        #             arr_mutation_gisaid = string_mut.split('","')
        #             seq_json['num_mut_gisaid'] = len(arr_mutation_gisaid)
        #
        #         seq_json['num_mut_loaded_equal_to_gisaid'] = 0
        #         seq_json['mut_loaded_different_from_gisaid'] = []
        #         for sin_mut in mutations:
        #             str_sin_mut = str(sin_mut)
        #             str_sin_mut = str_sin_mut.replace(' ', '')
        #             str_sin_mut = str_sin_mut.replace('\'', '')
        #             arr_mutation_loaded.append(str_sin_mut)
        #             if str_sin_mut in arr_mutation_gisaid:
        #                 seq_json['num_mut_loaded_equal_to_gisaid'] = seq_json['num_mut_loaded_equal_to_gisaid'] + 1
        #             else:
        #                 seq_json['mut_loaded_different_from_gisaid'].append(str_sin_mut)
        #         seq_json['num_mut_loaded'] = len(arr_mutation_loaded)
        #         if all_res2:
        #             seq_json['% equals'] = seq_json['num_mut_loaded_equal_to_gisaid']/seq_json['num_mut_gisaid']
        #         else:
        #             seq_json['% equals'] = 1
        #         seq_json['all_mut_gisaid'] = arr_mutation_gisaid
        #         seq_json['all_mut_loaded'] = arr_mutation_loaded
        #
        #         seq_mut_arr.append(seq_json)
        #
        # print("q", seq_mut_arr)

        statistics_input = {'arr_clu': array_cluster, 'stat_clu': statistics_cluster, 'arr_lin': array_lineage,
                            'stat_lin': statistics_lineage, 'stat_group': statistics_group_lineage,
                            'stat_group_mut': statistics_group_lineage_mut, 'stat_lin_mut': statistics_lineage_mut,
                            'stat_clu_mut': statistics_cluster_mut,
                            'stat_gr_c_mut_seq': statistics_group_count_mut_seq}
    #'sequence_mutation_arr': seq_mut_arr

        results = {'table': list_dict, 'stats': statistics_input}

        return results


###################################################  FUNZIONI ###################################################


def filter_metadata(metadata, selected_filters):
    metadata2 = defaultdict(dict)
    for seq in metadata:
        copy = True
        for key in metadata[seq]:
            value = metadata[seq][key]
            for metakey in selected_filters:
                if metakey == key:
                    if metakey == 'date':
                        min_date = selected_filters[metakey][0]['min_val']
                        max_date = selected_filters[metakey][0]['max_val']
                        if min_date is not None:
                            count = min_date.count('-')
                        elif max_date is not None:
                            count = max_date.count('-')
                        format = '%Y-%m-%d'
                        if min_date is not None:
                            if count == 1:
                                min_date = min_date + '-1'
                            date_min = datetime.datetime.strptime(min_date, format)
                        else:
                            date_min = None
                        if max_date is not None:
                            if count == 1:
                                arr_date = max_date.split('-')
                                month = int(arr_date[1])
                                if month == 4 or month == 6 or month == 9 or month == 11:
                                    max_date = max_date + '-30'
                                elif month == 2:
                                    max_date = max_date + '-28'
                                else:
                                    max_date = max_date + '-31'
                            date_max = datetime.datetime.strptime(max_date, format)
                        else:
                            date_max = None
                        value2 = datetime.datetime.strptime(value, '%Y-%m-%d')
                        if date_min is not None and value2 < date_min:
                            copy = False
                        if date_max is not None and value2 > date_max:
                            copy = False
                    else:
                        if value not in selected_filters[metakey]:
                            copy = False
        if copy:
            metadata2[seq] = metadata[seq]
    return metadata2

