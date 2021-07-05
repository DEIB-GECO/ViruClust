from __future__ import print_function

import http
import json

from scipy.stats import binom
from flask_restplus import Namespace, Resource


api = Namespace('analyze', description='analyze')

########################################################################################################


@api.route('/allGeo')
class FieldList(Resource):
    @api.doc('all_geo')
    def get(self):

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        conn.request('GET', '/virusurf_epitope/api/epitope/allGeo')

        response = conn.getresponse()
        all_geo = response.read().decode()
        all_geo = json.loads(all_geo)

        return all_geo


@api.route('/allLineages')
class FieldList(Resource):
    @api.doc('all_lineages')
    def get(self):

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        conn.request('GET', '/virusurf_epitope/api/epitope/allLineages')

        response = conn.getresponse()
        all_lin = response.read().decode()
        all_lin = json.loads(all_lin)

        return all_lin


@api.route('/allProtein')
class FieldList(Resource):
    @api.doc('all_protein')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/allProtein', json_data, headers)

        response = conn.getresponse()
        all_protein = response.read().decode()
        all_protein = json.loads(all_protein)

        return all_protein


@api.route('/tableLineageCountry')
class FieldList(Resource):
    @api.doc('table_lineage_country')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/tableLineageCountry', json_data, headers)

        response = conn.getresponse()
        all_geo = response.read().decode()
        all_geo = json.loads(all_geo)

        table = []
        for item in all_geo:
            single_line = {'lineage': item['lineage']}
            country_count = item['country_count']
            country_count = country_count.replace('"', "")
            country_count = country_count.replace("\\", "")
            country_count = country_count.replace("{", "")
            country_count = country_count.replace("}", "")
            country_count = country_count.replace("(", "")
            array_country_count = country_count.split("),")
            for single_country in array_country_count:
                single_country = single_country.replace(")", "")
                array_single_country = single_country.split(',')
                single_line[array_single_country[0]] = array_single_country[1]
            table.append(single_line)

        return table


@api.route('/possibleCountryLineage')
class FieldList(Resource):
    @api.doc('possible_country_lineage')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/arrayCountryForLineage', json_data, headers)

        response = conn.getresponse()
        all_country = response.read().decode()
        all_country = all_country.replace(']', '').replace('[', '')
        all_country = all_country.replace('"', '').split(",")

        return all_country


@api.route('/denominatorLineageCountry')
class FieldList(Resource):
    @api.doc('possible_country_lineage')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/denominatorLineageCountry', json_data, headers)

        response = conn.getresponse()
        resp = response.read().decode()
        resp = json.loads(resp)

        denominators = {}

        for item in resp:
            if item['geo'] is None:
                denominators['N/D'] = item['cnt']
            else:
                denominators[item['geo']] = item['cnt']

        return denominators


@api.route('/analyzeMutationCountryLineage')
class FieldList(Resource):
    @api.doc('analyze_mutation_country_lineage')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/analyzeMutationCountryLineage', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        mutation_table2 = []
        for item in all_result:
            single_item = {}
            if item['product'] == 'Spike (surface glycoprotein)':
                protein = item['product'].split(" ", 1)[0]
                mutation = protein + '_'
                # mutation = 'S_'
            else:
                protein = item['product'].split(" ", 1)[0]
                mutation = protein + '_'
            mutation += item['sequence_aa_original'] + str(item['start_aa_original']) + item['sequence_aa_alternative']
            single_item['mutation'] = mutation
            single_item['start_aa_original'] = item['start_aa_original']
            single_item['sequence_aa_original'] = item['sequence_aa_original']
            single_item['sequence_aa_alternative'] = item['sequence_aa_alternative']
            single_item['product'] = item['product']
            single_item['mutation_position'] = item['start_aa_original']
            single_item['target'] = item['country']
            single_item['background'] = item['lineage']
            single_item['count_target'] = item['count_seq']
            single_item['percentage_background'] = item['fraction']
            single_item['numerator_background'] = item['numerator']
            single_item['denominator_background'] = item['denominator']
            single_item['percentage_target'] = item['fraction_country']
            single_item['numerator_target'] = item['count_seq']
            single_item['denominator_target'] = item['denominator_country']

            epsilon = 0.00000001
            single_item['odd_ratio'] = (single_item['percentage_target'] + epsilon) / \
                                       (single_item['percentage_background'] + epsilon)

            if single_item['odd_ratio'] >= 1:
                single_item['p_value'] = 1 - binom.cdf(item['count_seq'] - 1, item['denominator_country'],
                                                   item['numerator'] / item['denominator'])
            else:
                single_item['p_value'] = binom.cdf(item['count_seq'], item['denominator_country'],
                                                       item['numerator'] / item['denominator'])

            mutation_table2.append(single_item)

        return mutation_table2


@api.route('/analyzeMutationCountryLineageInTime')
class FieldList(Resource):
    @api.doc('analyze_mutation_country_lineage_in_time')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/analyzeMutationCountryLineageInTime', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        mutation_table2 = []
        for item in all_result:
            single_item = {}
            if item['product'] == 'Spike (surface glycoprotein)':
                protein = item['product'].split(" ", 1)[0]
                mutation = protein + '_'
                # mutation = 'S_'
            else:
                protein = item['product'].split(" ", 1)[0]
                mutation = protein + '_'
            mutation += item['sequence_aa_original'] + str(item['start_aa_original']) + item['sequence_aa_alternative']
            single_item['mutation'] = mutation
            single_item['start_aa_original'] = item['start_aa_original']
            single_item['sequence_aa_original'] = item['sequence_aa_original']
            single_item['sequence_aa_alternative'] = item['sequence_aa_alternative']
            single_item['product'] = item['product']
            single_item['mutation_position'] = item['start_aa_original']
            single_item['target'] = item['target_time']
            single_item['background'] = item['background_time']
            single_item['country'] = item['country']
            single_item['lineage'] = item['lineage']
            single_item['count_target'] = item['count_seq']
            single_item['percentage_background'] = item['fraction']
            single_item['numerator_background'] = item['numerator']
            single_item['denominator_background'] = item['denominator']
            single_item['percentage_target'] = item['fraction_target']
            single_item['numerator_target'] = item['count_seq']
            single_item['denominator_target'] = item['denominator_target']

            epsilon = 0.00000001
            single_item['odd_ratio'] = (single_item['percentage_target'] + epsilon) / \
                                       (single_item['percentage_background'] + epsilon)

            if single_item['odd_ratio'] >= 1:
                single_item['p_value'] = 1 - binom.cdf(item['count_seq'] - 1, item['denominator_target'],
                                                       item['numerator'] / item['denominator'])
            else:
                single_item['p_value'] = binom.cdf(item['count_seq'], item['denominator_target'],
                                                       item['numerator'] / item['denominator'])

            mutation_table2.append(single_item)

        return mutation_table2


@api.route('/analyzeTimeDistributionCountryLineage')
class FieldList(Resource):
    @api.doc('analyze_time_distribution_country_lineage')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/analyzeTimeDistributionCountryLineage', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        return all_result


@api.route('/analyzeTimeDistributionBackgroundQueryGeo')
class FieldList(Resource):
    @api.doc('analyze_time_distribution_country_lineage')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/analyzeTimeDistributionBackgroundQueryGeo', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        return all_result


@api.route('/analyzeMutationProvinceRegion')
class FieldList(Resource):
    @api.doc('analyze_mutation_province_region')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/analyzeMutationProvinceRegion', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        mutation_table2 = []
        for item in all_result:
            single_item = {}
            if item['product'] == 'Spike (surface glycoprotein)':
                protein = item['product'].split(" ", 1)[0]
                mutation = protein + '_'
                # mutation = 'S_'
            else:
                protein = item['product'].split(" ", 1)[0]
                mutation = protein + '_'
            mutation += item['sequence_aa_original'] + str(item['start_aa_original']) + item['sequence_aa_alternative']
            single_item['start_aa_original'] = item['start_aa_original']
            single_item['sequence_aa_original'] = item['sequence_aa_original']
            single_item['sequence_aa_alternative'] = item['sequence_aa_alternative']
            single_item['mutation'] = mutation
            single_item['product'] = item['product']
            single_item['mutation_position'] = item['start_aa_original']
            # if 'country' in item:
            #    single_item['target'] = item['region']
            #    single_item['background'] = item['country']
            # else:
            #    single_item['target'] = item['province']
            #    single_item['background'] = item['region']
            single_item['target'] = item['target']
            single_item['background'] = item['background']

            single_item['lineage'] = item['lineage']
            single_item['count_target'] = item['count_seq']
            single_item['percentage_background'] = item['fraction']
            single_item['numerator_background'] = item['numerator']
            single_item['denominator_background'] = item['denominator']
            single_item['percentage_target'] = item['fraction_target']
            single_item['numerator_target'] = item['count_seq']
            single_item['denominator_target'] = item['denominator_target']

            epsilon = 0.00000001
            single_item['odd_ratio'] = (single_item['percentage_target'] + epsilon) / \
                                       (single_item['percentage_background'] + epsilon)

            if single_item['odd_ratio'] >= 1:
                single_item['p_value'] = 1 - binom.cdf(item['count_seq'] - 1, item['denominator_target'],
                                                       item['numerator'] / item['denominator'])
            else:
                single_item['p_value'] = binom.cdf(item['count_seq'], item['denominator_target'],
                                                       item['numerator'] / item['denominator'])

            mutation_table2.append(single_item)

        return mutation_table2


@api.route('/analyzeMutationTargetBackgroundFree')
class FieldList(Resource):
    @api.doc('analyze_mutation_target_background_free')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/analyzeMutationTargetBackgroundFree', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        mutation_table2 = []
        for item in all_result:
            single_item = {}
            if item['product'] == 'Spike (surface glycoprotein)':
                protein = item['product'].split(" ", 1)[0]
                mutation = protein + '_'
                # mutation = 'S_'
            else:
                protein = item['product'].split(" ", 1)[0]
                mutation = protein + '_'
            mutation += item['sequence_aa_original'] + str(item['start_aa_original']) + item['sequence_aa_alternative']
            single_item['start_aa_original'] = item['start_aa_original']
            single_item['sequence_aa_original'] = item['sequence_aa_original']
            single_item['sequence_aa_alternative'] = item['sequence_aa_alternative']
            single_item['mutation'] = mutation
            single_item['product'] = item['product']
            single_item['mutation_position'] = item['start_aa_original']
            single_item['target'] = item['target']
            single_item['background'] = item['background']

            single_item['lineage'] = item['lineage']
            single_item['count_target'] = item['count_seq']
            single_item['percentage_background'] = item['fraction']
            single_item['numerator_background'] = item['numerator']
            single_item['denominator_background'] = item['denominator']
            single_item['percentage_target'] = item['fraction_target']
            single_item['numerator_target'] = item['count_seq']
            single_item['denominator_target'] = item['denominator_target']

            epsilon = 0.00000001
            single_item['odd_ratio'] = (single_item['percentage_target'] + epsilon) / \
                                       (single_item['percentage_background'] + epsilon)

            if single_item['odd_ratio'] >= 1:
                if item['denominator'] != 0:
                    single_item['p_value'] = 1 - binom.cdf(item['count_seq'] - 1, item['denominator_target'],
                                                       item['numerator'] / item['denominator'])
                else:
                    single_item['p_value'] = 0
            else:
                if item['denominator'] != 0:
                    single_item['p_value'] = binom.cdf(item['count_seq'], item['denominator_target'],
                                                       item['numerator'] / item['denominator'])
                else:
                    single_item['p_value'] = 0

            mutation_table2.append(single_item)

        return mutation_table2


@api.route('/countOverlappingSequenceTargetBackground')
class FieldList(Resource):
    @api.doc('count_overlapping_sequence_target_background')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/countOverlappingSequenceTargetBackground', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        return all_result


@api.route('/selectorQuery')
class FieldList(Resource):
    @api.doc('selector_query')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/selectorQuery', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        return all_result


@api.route('/getAccessionIds')
class FieldList(Resource):
    @api.doc('selector_query')
    def post(self):

        to_send = api.payload

        conn = http.client.HTTPConnection('geco.deib.polimi.it')
        headers = {'Content-type': 'application/json'}
        send = to_send
        json_data = json.dumps(send)
        conn.request('POST', '/virusurf_epitope/api/epitope/getAccessionIds', json_data, headers)

        response = conn.getresponse()
        all_result = response.read().decode()
        all_result = json.loads(all_result)

        return all_result
