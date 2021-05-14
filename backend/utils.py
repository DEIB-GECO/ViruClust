import datetime
import json
import os
import time
from collections import OrderedDict

import sqlalchemy
from flask import request

center_table = 'Sequence'
center_table_id = 'sequence_id'

# the view order definitions
views = {
    'biological_v': [center_table, 'Virus'],
    'biological_h': [center_table, 'HostSample'],
    'technological': [center_table, 'ExperimentType'],
    'organizational': [center_table, 'SequencingProject'],
    'analytical_a': [center_table, 'Annotation', 'AminoacidVariant'],
    'analytical_impact': [center_table, 'NucleotideVariantAnnotated', 'VariantImpact'],
    'view_annotation': [center_table, 'AnnotationView'],

}


def get_view(table):
    if table == "Sequence":
        return "technological"
    for view_name, view_tables in views.items():
        if table in view_tables:
            return view_name


class Column:

    def __init__(self, table_name, column_name, column_type, has_tid=False, description="", title=None,
                 is_numerical=False, is_date=False):
        self.table_name = table_name
        self.column_name = column_name
        self.column_type = column_type
        self.has_tid = has_tid
        self.description = description
        self.title = title
        self.view = get_view(table_name)
        self.is_numerical = is_numerical
        self.is_date = is_date

    def var_table(self):
        return var_table(self.table_name)

    def var_column(self):
        return self.column_name[:2].lower()

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


def var_table(table_name):
    return table_name[:2].lower()


def unfold_list(res):
    return [item for sublist in res for item in sublist]


def calc_distance(view_name, pre_table, table_name):
    view = views[view_name]
    if view_name == 'analytical_a':
        return 2
    return view.index(table_name) - view.index(pre_table)


columns = [
    # technological
    Column('Sequence', 'is_reference', bool, False,
           "True when the sequence is the reference one (from RefSeq) for the virus species, False when the sequence is not the reference one"),
    Column('Sequence', 'is_complete', bool, False,
           "True when the sequence is complete, False when the sequence is partial. When not available from original source, "
           "we set False if its length is less than 95% of the reference sequence length, otherwise we set N/D since completeness cannot be determined with needed accuracy."),
    Column('Sequence', 'strand', str, False, "Strand to which the sequence belongs to (either positive or negative)"),
    Column('Sequence', 'length', int, False, "Number of nucleotides of the sequence", "Sequence Length",
           is_numerical=True),
    Column('Sequence', 'gc_percentage', float, False, "Percentage of read G and C bases", "GC%", is_numerical=True),
    Column('Sequence', 'n_percentage', float, False, "Percentage of unknown bases", "N%", is_numerical=True),
    Column('Sequence', 'lineage', str, False, "Sequence lineage derived from source (for COG-UK) or calculated with the Pangolin software https://cov-lineages.org/pangolin.html (for other sources)"),

    Column('ExperimentType', 'sequencing_technology', str, False, "Platform used for the sequencing experiment"),
    Column('ExperimentType', 'assembly_method', str, False,
           "Algorithms applied to obtain the final sequence (e.g., for reads assembly, reads alignment, variant calling)"),
    Column('ExperimentType', 'coverage', int, False,
           "Number of unique reads that include a specific nucleotide in the reconstructed sequence",
           is_numerical=True),

    # organizational
    Column('SequencingProject', 'sequencing_lab', str, False,
           "Laboratory that sequenced and submitted the sequence to the databank (encoded by \'Database source\')",
           "Submitting Lab"),
    Column('SequencingProject', 'submission_date', datetime, False,
           "Date of submission of the sequence to the databank (encoded by \'Database source\')",
           is_date=True),
    Column('SequencingProject', 'bioproject_id', str, False,
           "External reference to the NCBI BioProject database https://www.ncbi.nlm.nih.gov/bioproject/",
           "BioProject ID"),
    Column('SequencingProject', 'database_source', str, False, "Original database from which information is collected"),

    # biological
    Column('Virus', 'taxon_id', int, False,
           "Virus numerical id as to the NCBI Taxonomy https://www.ncbi.nlm.nih.gov/taxonomy", "Virus taxon ID"),
    Column('Virus', 'taxon_name', str, False,
           "Virus name as to the NCBI Taxonomy https://www.ncbi.nlm.nih.gov/taxonomy", "Virus taxon name"),
    Column('Virus', 'species', str, False,
           "Virus species name as to the NCBI Taxonomy https://www.ncbi.nlm.nih.gov/taxonomy", "Virus species"),

    Column('HostSample', 'host_taxon_name', str, False,
           "Host organism species name from NCBI Taxonomy https://www.ncbi.nlm.nih.gov/taxonomy", "Host taxon name"),
    Column('HostSample', 'collection_date', datetime, False,
           "Date in which the infected biological sample was collected", is_date=True),
    Column('HostSample', 'isolation_source', str, False,
           "Tissue from which the infected biological sample was collected"),
    Column('HostSample', 'geo_group', str, False, "Continent where the biological sample was collected", "Continent"),
    Column('HostSample', 'country', str, False, "Country where the biological sample was collected"),
    Column('HostSample', 'region', str, False,
           "Region (i.e., part of country) where the biological sample was collected"),
    Column('HostSample', 'gender', str, False, "Host organism gender (when applicable)"),
    Column('HostSample', 'age', int, False, "Host organism age (in years, when applicable) ", is_numerical=True),
]

columns_item = [
    Column('Sequence', 'accession_id', str, False, "Sequence unique identifier, from original source database",
           "Accession ID"),
    Column('Sequence', 'strain_name', str, False,
           "Virus strain name (sometimes hard-coding relevant information such as the species, collection location and date)"),

    # Column('Sequence', 'nucleotide_sequence', str, False, ""),
    Column('Sequence', 'clade', str, False, "Sequence-clade description"),
    Column('HostSample', 'host_taxon_id', int, False, "HostSample-host_taxon_id description"),
    Column('HostSample', 'originating_lab', str, False, "HostSample-originating_lab description"),
    Column('Virus', 'genus', str, False, "Virus-genus description"),
    Column('Virus', 'sub_family', str, False, "Virus-sub_family description"),
    Column('Virus', 'family', str, False, "Virus-family description"),
    Column('Virus', 'equivalent_list', str, False, "Virus-equivalent_list description"),
    Column('Virus', 'molecule_type', str, False, "Virus-molecule_type description"),
    Column('Virus', 'is_single_stranded', str, False, "Virus-is_single_stranded description"),
    Column('Virus', 'is_positive_stranded', str, False, "Virus-is_positive_stranded description"),

    Column('AnnotationView', 'aminoacid_sequence', str, False,
           "Virus-is_positive_stranded description"),
    Column('AnnotationView', 'annotation_nucleotide_sequence', str, False,
           "Virus-is_positive_stranded description"),
]

columns_others = [
    Column('Annotation', 'gene_name', str, False, "Annotation-gene_name description"),
    Column('Annotation', 'product', str, False, "Annotation-product description"),

    Column('AminoacidVariant', 'variant_aa_type', str, False, "Annotation-variant_aa_type description"),
    Column('AminoacidVariant', 'sequence_aa_original', str, False, "Annotation-sequence_aa_original description"),
    Column('AminoacidVariant', 'sequence_aa_alternative', str, False, "Annotation-sequence_aa_alternative description"),
    # Column('AminoacidVariant', 'aa_position', int, False, "AminoacidVariant-aa_position"),
    Column('AminoacidVariant', 'start_aa_original', int, False, "AminoacidVariant-start_aa_original"),

    Column('NucleotideVariantAnnotated', 'sequence_original', str, False,
           "NucleotideVariant-sequence_original description"),
    Column('NucleotideVariantAnnotated', 'sequence_alternative', str, False,
           "NucleotideVariant-sequence_alternative description"),
    Column('NucleotideVariantAnnotated', 'variant_type', str, False,
           "NucleotideVariant-variant_type description"),
    # Column('NucleotideVariant', 'var_position', int, False, "NucleotideVariant-var_position"),
    Column('NucleotideVariantAnnotated', 'start_original', int, False, "NucleotideVariant-var_position"),
    Column('NucleotideVariantAnnotated', 'variant_length', int, False, "NucleotideVariant-variant_length"),

    Column('NucleotideVariantAnnotated', 'n_feature_type', str, False,
           "NucleotideVariantAnnotation-n_feature_type description"),
    Column('NucleotideVariantAnnotated', 'n_gene_name', str, False,
           "NucleotideVariantAnnotation-n_gene_name description"),
    Column('NucleotideVariantAnnotated', 'n_product', str, False,
           "NucleotideVariantAnnotation-n_product description"),

    Column('VariantImpact', 'effect', str, False,
           "VariantImpact-effect description"),
    Column('VariantImpact', 'putative_impact', str, False,
           "VariantImpact-putative_impact description"),
    Column('VariantImpact', 'impact_gene_name', str, False,
           "VariantImpact-impact_gene_name description"),

    Column('AnnotationView', 'annotation_view_product', str, False, "annotation_view_product description"),
]

columns_dict = {x.column_name: x for x in columns}

columns_dict_item = {x.column_name: x for x in columns + columns_item}

columns_dict_all = {x.column_name: x for x in columns + columns_item + columns_others}

del columns
del columns_item
del columns_others

# TODO uncomment if there are replications on the management view,
#  and create a query that takes care for different views
# TODO VIRUS
agg_tables = []  # views['biological'][1:]  # +views['management'][1:]


def pair_query_resolver(pair_query, pair_key):
    # print(pair_query)
    where_temp_inner = []
    for name, val in pair_query.items():
        search_list = [
            ('Annotation', f"ann{pair_key}"),
            ('AminoacidVariant', f"aa_var{pair_key}"),
            ('NucleotideVariantAnnotated', f"n_var{pair_key}"),
            ('VariantImpact', f"n_imp{pair_key}"),
        ]
        inner_table_name = ''
        for t_name, t_alias in search_list:
            if name in [x.column_name for x in columns_dict_all.values() if x.table_name == t_name]:
                inner_table_name = t_alias
                break

        if name == 'start_aa_original':
            position_sub = []
            if 'min_val' in val:
                position_sub.append(f" aa_var{pair_key}.start_aa_original >= {int(val['min_val'])} ")
            if 'max_val' in val:
                position_sub.append(f" aa_var{pair_key}.start_aa_original <= {int(val['max_val'])} ")
            where_temp_inner.append(f" ({' AND '.join(position_sub)}) ")
        elif name == 'start_original':
            position_sub = []
            if 'min_val' in val:
                position_sub.append(f" n_var{pair_key}.start_original >= {int(val['min_val'])} ")
            if 'max_val' in val:
                position_sub.append(f" n_var{pair_key}.start_original <= {int(val['max_val'])} ")
            where_temp_inner.append(f" ({' AND '.join(position_sub)}) ")
        elif name == 'variant_length':
            variant_length_sub = []
            if 'min_val' in val:
                variant_length_sub.append(f" n_var{pair_key}.variant_length >= {int(val['min_val'])} ")
            if 'max_val' in val:
                variant_length_sub.append(f" n_var{pair_key}.variant_length <= {int(val['max_val'])} ")
            where_temp_inner.append(f" ({' AND '.join(variant_length_sub)}) ")
        else:
            inner_text_list = []
            if None in val:
                inner_text_list.append(f" lower({inner_table_name}.{name}) IS NULL ")
            vals = ",".join([f"'{x.lower()}'" for x in val if x])
            if vals:
                inner_text_list.append(f" lower({inner_table_name}.{name}) IN ({vals}) ")
            where_temp_inner.append("(" + " OR ".join(inner_text_list) + ")")
    return "(" + " AND ".join(where_temp_inner) + ")"


def sql_query_generator(gcm_query, search_type, pairs_query, return_type, agg=False, field_selected="", limit=1000,
                        offset=0, order_col="accession_id", order_dir="ASC", rel_distance=3, panel=None,
                        annotation_type=None, external_where_conditions=[], with_nuc_seq = False, epitope_part=None,
                        epitope_table=None):
    # TODO VIRUS PAIRS
    # pairs = generate_where_pairs(pairs_query)
    # pairs = generate_where_pairs({})
    pair_join = ''
    pair_where = ''
    pair_count = []

    where_temp_outer_and = []
    # if pairs_query:
    for pair_key, pair_value in pairs_query.items():
        # print("pair_key:", pair_key)
        # print("pairs_query:", pairs_query)
        type_query = pair_value['type_query']
        # print('type_query', type_query)
        pair_queries = pair_value['query']
        # print('pair_queries', pair_queries)

        tables = set(y for x in pair_value['query'] for y in x.keys())
        if type_query == 'aa':
            pair_count.append(f" COUNT(DISTINCT aa_var{pair_key}.aminoacid_variant_id) {pair_key}_count ")
            pair_join += f" JOIN annotation as ann{pair_key} ON ann{pair_key}.sequence_id = it.sequence_id "
            # if tables.intersection([x.column_name for x in columns_dict_all.values() if x.table_name == 'AminoacidVariant']):
            pair_join += f" JOIN aminoacid_variant as aa_var{pair_key} ON aa_var{pair_key}.annotation_id = ann{pair_key}.annotation_id "
        if type_query == 'nuc':
            pair_count.append(f" COUNT(DISTINCT n_var{pair_key}.nucleotide_variant_id) {pair_key}_count ")
            pair_join += f" JOIN nucleotide_variant_annotated as n_var{pair_key} ON n_var{pair_key}.sequence_id = it.sequence_id "
            if tables.intersection(
                    [x.column_name for x in columns_dict_all.values() if x.table_name == 'VariantImpact']):
                pair_join += f" JOIN variant_impact as n_imp{pair_key} ON n_imp{pair_key}.nucleotide_variant_id = n_imp{pair_key}.nucleotide_variant_id "

        where_temp_outer_or = []
        for pair_query in pair_queries:
            pair_query_res = pair_query_resolver(pair_query, pair_key)
            where_temp_outer_or.append(pair_query_res)
        where_temp_outer_and.append("(" + " OR ".join(where_temp_outer_or) + ")")

    pair_where += " AND ".join(where_temp_outer_and)

    print('pair_join: ', pair_join)
    print('pair_where: ', pair_where)

    select_part = ""
    from_part = ""
    item = " FROM sequence it "
    # dataset_join = " join dataset da on it.dataset_id = da.dataset_id "

    if with_nuc_seq:
        item += " NATURAL JOIN nucleotide_sequence as nuc_seq"

    experiment_type_join = " join experiment_type ex on it.experiment_type_id = ex.experiment_type_id"

    sequencing_project_join = " join sequencing_project sp on it.sequencing_project_id = sp.sequencing_project_id"

    host_sample_join = " join host_sample_view hs on it.host_sample_id = hs.host_sample_id"

    virus_join = " join virus v on it.virus_id = v.virus_id"

    annotation_join = " JOIN annotation as ann ON it.sequence_id = ann.sequence_id "

    aminoacid_variant_join = " JOIN aminoacid_variant as aa_var ON aa_var.annotation_id = ann.annotation_id "

    nucleotide_variant_join = " JOIN nucleotide_variant_annotated as n_var ON it.sequence_id = n_var.sequence_id "

    nucleotide_variant_impact = " JOIN variant_impact as n_imp ON n_var.nucleotide_variant_id = n_imp.nucleotide_variant_id "

    annotation_view_join = " JOIN annotation_sequence as ann_view ON it.sequence_id = ann_view.sequence_id "

    view_join = {
        # TODO VIRUS
        'biological_h': [host_sample_join],
        'biological_v': [virus_join],
        'organizational': [sequencing_project_join],
        'technological': [experiment_type_join],
        'analytical_a': [annotation_join, aminoacid_variant_join],
        'analytical_impact': [nucleotide_variant_join, nucleotide_variant_impact],
        'view_annotation': [annotation_view_join],
    }

    if field_selected != "" or return_type == 'item_id':
        columns = [x for x in gcm_query.keys()]
        if field_selected != "":
            columns.append(field_selected)
        if panel:
            for key_panel in panel:
                columns.append(key_panel)
        tables = [columns_dict_all[x].table_name for x in columns]
        joins = []
        for table in tables:
            # table = columns_dict_item[field_selected].table_name
            view = get_view(table)
            index = calc_distance(view, center_table, table)
            joins += view_join[view][:index]
        joins = list(OrderedDict.fromkeys(joins))
        from_part = item + " ".join(joins) + pair_join
    else:
        from_part = item + experiment_type_join + sequencing_project_join + host_sample_join + virus_join + pair_join
        if annotation_type:
            annotation_type = annotation_type.replace("'", "''")
            from_part = from_part + annotation_view_join + f" AND lower(ann_view.product) = lower('{annotation_type}')"

    gcm_where = generate_where_sql(gcm_query, search_type, rel_distance=rel_distance, epitope_part=epitope_part, epitope_table=epitope_table)

    panel_where = ''
    if panel:
        panel_where = pair_query_resolver(panel, '')

    where_part = ""
    where_list = [x for x in [gcm_where, pair_where, panel_where] + external_where_conditions if x]

    if where_list:
        where_part = " WHERE " + " AND ".join(where_list)

    # print("where_part:", where_part)
    for i, wp in enumerate(where_list):
        print(f"where_sub_part({i}):", wp)

    sub_where_part = ""
    group_by_part = ""
    limit_part = ""
    offset_part = ""
    order_by = ""
    if return_type == 'table':
        if annotation_type:
            select_columns = columns_dict_item.keys()
        else:
            select_columns = (key for key, value in columns_dict_item.items() if value.table_name != 'AnnotationView')

        all_columns = "it.sequence_id, " + ', '.join(select_columns) + " "
        select_part = "SELECT " + ("max(nuc_seq.nucleotide_sequence) as nucleotide_sequence, " if with_nuc_seq else "") + all_columns
        if pair_count:
            select_part += ',' + ','.join(pair_count)

        group_by_part = " GROUP BY " + all_columns
        del all_columns

        if limit:
            limit_part = f" LIMIT {limit} "
        if offset:
            offset_part = f"OFFSET {offset} "
        order_by = f" ORDER BY {order_col} {order_dir} "

    elif return_type == 'allInfo':
        select_part = " SELECT * "

    elif return_type == 'allInfoCustomEpi':
        select_part = " SELECT distinct it.*, ex.*, sp.*, hs.*, v.*, annaa_0.*, aa_varaa_0.* "

    elif return_type == 'field_value':
        # TODO add new....
        if columns_dict_all[field_selected].table_name == 'Annotation':
            field_selected_new = "ann." + field_selected
        elif columns_dict_all[field_selected].table_name == 'AminoacidVariant':
            field_selected_new = "aa_var." + field_selected
        elif columns_dict_all[field_selected].table_name == 'NucleotideVariantAnnotated':
            field_selected_new = "n_var." + field_selected
        elif columns_dict_all[field_selected].table_name == 'VariantImpact':
            field_selected_new = "n_imp." + field_selected
        elif field_selected == "annotation_view_product":
             field_selected_new ="ann_view.product"
        else:
            field_selected_new = field_selected

        col = columns_dict_all[field_selected]
        column_type = col.column_type
        lower_pre = 'LOWER(' if column_type == str else ''
        lower_post = ')' if column_type == str else ''
        distinct = ""
        # if search_type == 'original':
        distinct = "distinct"
        select_part = f"SELECT {distinct} {lower_pre}{field_selected_new}{lower_post} as label, it.{center_table_id} as item "

    elif return_type == 'item_id':
        select_part = f"SELECT DISTINCT it.{center_table_id} "

    elif return_type == 'count_variants':
        select_part = f"SELECT distinct aa_varaa_0.aminoacid_variant_id, aa_varaa_0.variant_aa_length "

    full_query = select_part + from_part + where_part + sub_where_part + group_by_part + order_by + limit_part + offset_part
    print(full_query)
    return full_query


def generate_where_sql(gcm_query, search_type, rel_distance=3, epitope_part=None, epitope_table=None):
    sub_where = []
    where_part = ""
    if gcm_query:
        where_part = " ("

    for (column, values) in gcm_query.items():
        col = columns_dict_item[column]
        column_type = col.column_type
        lower_pre = 'LOWER(' if column_type == str else ''
        lower_post = ')' if column_type == str else ''
        syn_sub_where = []

        if search_type == 'synonym' and col.has_tid:
            syn_sub_where = [f"{col.column_name}_tid in (SELECT tid FROM synonym WHERE LOWER(label) = LOWER('{value}'))"
                             for
                             value in values
                             if value is not None]
        elif search_type == 'expanded' and col.has_tid:
            syn_sub_where = [f"{col.column_name}_tid in (SELECT tid_descendant "
                             f"FROM relationship_unfolded WHERE distance <= {rel_distance} and tid_ancestor in "
                             f"(SELECT tid FROM synonym WHERE LOWER(label) = LOWER('{value}')))" for
                             value in values
                             if value is not None]
        if col.is_numerical or col.is_date:

            min = values.get('min_val')
            max = values.get('max_val')
            isNull = values.get('is_null')
            a = ""

            if min is not None:
                if col.is_date:
                    a += f" {col.column_name} >= '{min}' "
                else:
                    a += f" {col.column_name} >= {min} "

            if max is not None:
                if a:
                    a += ' and '
                if col.is_date:
                    a += f" {col.column_name} <= '{max}' "
                else:
                    a += f" {col.column_name} <= {max} "

            if isNull:
                if a:
                    a += ' or '
                a += f" {col.column_name} is null "

            if not a:
                a += ' TRUE '

            sub_where.append(a)

        else:
            sub_sub_where = [f"{lower_pre}{column}{lower_post} = '{value}'" for value in values if value is not None]
            sub_sub_where_none = [f"{column} IS NULL" for value in values if value is None]
            sub_sub_where.extend(sub_sub_where_none)
            sub_sub_where.extend(syn_sub_where)
            sub_where.append(" OR ".join(sub_sub_where))

    if gcm_query:
        where_part += ") AND (".join(sub_where) + ")"

    if epitope_part is not None:
        where_part += f""" and it.sequence_id IN (SELECT distinct sequence_id 
                        FROM {epitope_table} as epic  {epitope_part}) """
    return where_part


def generate_where_pairs(pair_query):
    searched = pair_query.keys()

    pair_join = []

    where = []
    i = 0
    for x in searched:
        kv = "kv_" + str(i)
        i += 1
        join = f" join unified_pair {kv} on it.{center_table_id} = {kv}.{center_table_id} "
        pair_join.append(join)
        items = pair_query[x]['query']
        gcm = items['gcm']
        pair = items['pairs']

        sub_where = []

        for k in gcm.keys():
            a = ""
            a += f" lower({kv}.key) = lower('{k}') and {kv}.is_gcm = true and "
            values = gcm[k]
            sub_sub_where = []
            for value in values:
                v = value.replace("'", "''")
                sub_sub_where.append(f"lower({kv}.value) = lower('{v}')")
            a += ("(" + " OR ".join(sub_sub_where) + ")")

            # print(a)
            sub_where.append(a)

        for k in pair.keys():
            a = ""
            a += f" lower({kv}.key) = lower('{k}') and {kv}.is_gcm = false and "
            values = pair[k]
            sub_sub_where = []
            for value in values:
                v = value.replace("'", "''")
                sub_sub_where.append(f"lower({kv}.value) = lower('{v}')")
            a += ("(" + " OR ".join(sub_sub_where) + ")")

            # print(a)
            sub_where.append(a)

        where.append("(" + ") OR (".join(sub_where) + ")")

    where_part = ""
    if pair_query:
        where_part = "(" + ") AND (".join(where) + ")"

    return {'where': where_part, 'join': " ".join(pair_join)}


# IP ADDRESS AND QUERY LOGGING

ROOT_DIR = os.path.dirname(os.getcwd())
if not os.path.exists(ROOT_DIR + "/logs"):
    os.makedirs(ROOT_DIR + "/logs")
fn = ROOT_DIR + "/logs/count.log"
f = open(fn, 'a+')
header = "timestamp\tIP_address\tendpoint\tquery\tpayload\n"

f.seek(0)
firstline = f.read()

if firstline == '':
    f.write(header)

f.close()


def log_query(endpoint, q, payload):
    if 'HTTP_X_REAL_IP' in request.environ:
        addr = request.environ['HTTP_X_REAL_IP']
    else:
        addr = request.remote_addr
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data = timestamp + "\t" + addr + "\t" + endpoint + "\t" + q + "\t" + str(payload) + "\n"
    fi = open(fn, 'a+')
    fi.write(data)
    fi.close()


def ip_info(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    # response from url(if res==None then check connection)
    data = load(res)
    # will load the json response into data
    for attr in data.keys():
        # will print the data line by line
        print(attr, ' ' * 13 + '\t->\t', data[attr])
    print(data)


taxon_name_dict = {}
taxon_id_dict = {}


def load_viruses():
    from app import my_app
    from model.models import db
    try:
        import json
        with open("viz_color.json", "r") as f:
            product_colors = json.load(f)
            product_colors = {int(key): val for key, val in product_colors.items()}
    except:
        product_colors = {}
    with my_app.app_context():
        query = sql_query_generator({"is_reference": [True]}, "original", {}, 'table', limit=None)
        pre_query = db.engine.execute(sqlalchemy.text(query))
        # return_columns = pre_query._metadata.keys
        # print(return_columns)
        res = pre_query.fetchall()
        for row in res:
            row_dict = dict(row)
            taxon_name = row_dict['taxon_name'].lower()
            taxon_id = row_dict['taxon_id']
            # add two empty lists (AA and nuc) to use below
            row_dict.update({#'nucleotide_sequence_length': len(row_dict['nucleotide_sequence']),
                             "a_products": list(),
                             "n_products": list(), })

            row_dict = {k: v for k, v in row_dict.items() if k in ["taxon_id",
                                                                   "taxon_name",
                                                                   "a_products",
                                                                   "n_products",
                                                                   # "nucleotide_sequence_length",
                                                                   ]}
            taxon_name_dict[taxon_name] = row_dict
            taxon_id_dict[taxon_id] = row_dict

        query = """
            SELECT  *,
                MIN(start) OVER(PARTITION BY gene_name) = start AND
                MAX(stop) OVER(PARTITION BY gene_name) = stop as is_gene 
            FROM virus 
            NATURAL JOIN sequence
            NATURAL JOIN annotation
            NATURAL LEFT JOIN annotation_sequence
            WHERE is_reference
            ORDER BY virus_id, gene_name
        """
        pre_query = db.engine.execute(sqlalchemy.text(query))
        # return_columns = pre_query._metadata.keys
        # print(return_columns)
        res = pre_query.fetchall()
        for row in res:
            row_dict = dict(row)
            taxon_id = row_dict['taxon_id']
            product = row_dict["product"]

            a_new_product = {
                "name": product,
                "start": row_dict["start"],
                "end": row_dict["stop"],
                "row": 0,
                "sequence": row_dict["aminoacid_sequence"],
            }
            if taxon_id in product_colors and product in product_colors[taxon_id]:
                a_new_product.update({'color': product_colors[taxon_id][product]})

            taxon_id_dict[taxon_id]["a_products"].append(a_new_product)

            if row_dict["is_gene"]:
                n_new_product = {
                    "name": row_dict["gene_name"],
                    "start": row_dict["start"],
                    "end": row_dict["stop"],
                    "row": 0,
                }
                taxon_id_dict[taxon_id]["n_products"].append(n_new_product)


connection_dict = {}


def custom_db_execution(query, poll_id):
    from threading import Timer
    from app import my_app
    from model.models import db

    with db.engine.connect() as connection:

        def drop():
            forget_connection(poll_id, connection)

        save_connection(poll_id, connection)
        t = Timer(5.0, drop)
        t.start()
        pre_query = connection.execute(query)
        results = pre_query.fetchall()
        connection.close()
        #forget_connection(poll_id, connection)
        return results


def save_connection(poll_id, connection):
    new_connection = {
        "poll_id": poll_id,
        "connection": connection
    }
    new_connection_line = dict(new_connection)
    connection_dict[poll_id] = new_connection_line


def forget_connection(poll_id, conn):
    #conn.close()
    connection_dict.pop(poll_id)
