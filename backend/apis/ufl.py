import json
import urllib

import requests
import http.client

from flask_restplus import Namespace, Resource


api = Namespace('ufl', description='ufl')

http.client._MAXLINE = 655360

########################################################################################################


@api.route('')
class FieldList(Resource):
    @api.doc('get_field_list')
    def get(self):
        response = requests.get("http://geco.deib.polimi.it/virusurf_epitope/api/epitope/allEpitopes")
        myobj = [('c101', 'B.1'), ('c103', 'B.1.243')]

        url = 'http://geco.deib.polimi.it/virusurf_epitope/api/epitope/statisticsMutationsLineages'

        myobj2 = [('c101', 'B.1'), ('c103', 'B.1.243'), ('c114', 'B.1.240'), ('c12', 'B.1.351'), ('c122', 'B.1'), ('c125', 'B.1.381'), ('c126', 'B.1.381'), ('c128', 'B.1.381'), ('c129', 'B.1.381'), ('c131', 'B.1.237'), ('c133', 'A'), ('c133', 'B'), ('c133', 'B.23'), ('c133', 'B.29'), ('c133', 'B.3'), ('c133', 'B.39'), ('c133', 'B.40'), ('c133', 'B.52'), ('c133', 'B.6'), ('c14', 'B.1.351'), ('c149', 'B.1.1.254'), ('c151', 'B.1.1.254'), ('c153', 'B.1'), ('c153', 'B.1.1.254'), ('c153', 'B.1.1.269'), ('c163', 'B.1.1.119'), ('c176', 'B.1.1.117'), ('c182', 'B.1.1.119'), ('c182', 'B.1.1.220'), ('c199', 'B.1.1.84'), ('c203', 'B.1.1.34'), ('c204', 'B.1.1.34'), ('c208', 'B.1.1.62'), ('c210', 'B.1.1.314'), ('c210', 'B.1.1.33'), ('c211', 'B.1.1.216'), ('c211', 'B.1.1.4'), ('c211', 'B.1.1.75'), ('c217', 'B.1.1.109'), ('c221', 'B.1.1.7'), ('c224', 'H.1'), ('c225', 'B.1.1.67'), ('c227', 'B.1.1.53'), ('c228', 'B.1.1.53'), ('c240', 'C.1'), ('c242', 'C.1'), ('c255', 'C.9'), ('c257', 'C.9'), ('c259', 'B.1.1.1'), ('c259', 'C.2'), ('c260', 'B.1.1.1'), ('c263', 'B.1.1.1'), ('c269', 'B.1.1.1'), ('c28', 'B.1.351'), ('c282', 'B.1.1.57'), ('c285', 'B.1.1.57'), ('c289', 'B.1.1.311'), ('c29', 'B.1.351'), ('c290', 'B.1.1.309'), ('c291', 'B.1.1.119'), ('c291', 'B.1.1.52'), ('c293', 'B.1.1.281'), ('c293', 'B.1.1.306'), ('c299', 'B.1.1.273'), ('c301', 'B.1.1.273'), ('c301', 'B.1.146'), ('c310', 'H.1'), ('c320', 'B.1.1.67'), ('c320', 'H.1'), ('c326', 'B.1.1.56'), ('c329', 'B.1.1.119'), ('c329', 'B.1.1.208'), ('c329', 'B.1.1.37'), ('c329', 'B.1.1.62'), ('c334', 'B.1.1.206'), ('c342', 'B.1.1.206'), ('c347', 'B.1.1.206'), ('c350', 'B.1.1.206'), ('c371', 'B.1.1.206'), ('c375', 'B.1.1.206'), ('c375', 'B.1.1.54'), ('c379', 'B.1.1.206'), ('c38', 'B.1.351'), ('c384', 'B.1.1.206'), ('c389', 'B.1.1.206'), ('c39', 'B.1.351'), ('c4', 'B.1.351'), ('c45', 'B.1.351'), ('c46', 'B.1.351'), ('c47', 'B.1.351'), ('c49', 'B.1.351'), ('c65', 'B.1.140'), ('c72', 'B.1.106'), ('c73', 'B.1.106'), ('c78', 'B.1.177'), ('c78', 'B.1.177.1'), ('c78', 'B.1.177.12'), ('c78', 'B.1.177.14'), ('c78', 'B.1.177.16'), ('c78', 'B.1.177.18'), ('c78', 'B.1.177.24'), ('c93', 'B.1'), ('c93', 'B.1.157'), ('c93', 'B.1.237'), ('c97', 'B.1'), ('c99', 'B.1.417')]



        conn = http.client.HTTPConnection('geco.deib.polimi.it')

        headers = {'Content-type': 'application/json'}

        foo = myobj2
        json_data = json.dumps(foo)

        conn.request('GET', '/virusurf_epitope/api/epitope/statisticsMutationsLineagesGET')

        response2 = conn.getresponse()
        res = response2.read().decode()
        # print(res)
        # print("len", len(res))

        lineage_stats = json.loads(res)

        # def test():
        #     with requests.post(url, data=myobj2, stream=True) as r:
        #         for chunk in r.iter_lines(decode_unicode=True):
        #             decoded_line = chunk.decode('utf-8')
        #             yield decoded_line
        #
        # aaa = test()
        # x = json.loads(''.join(aaa))

        res = {'res1': response.json(), 'res2': lineage_stats}

        return res

