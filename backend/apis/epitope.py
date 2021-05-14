
from flask_restplus import Namespace, Resource, fields, inputs


is_gisaid = False
epitope_id = 'iedb_epitope_id'

api = Namespace('epitope', description='epitope')

query = api.model('epitope', {
})

table_parser = api.parser()
table_parser.add_argument('page', type=int)
table_parser.add_argument('num_elems', type=int)
table_parser.add_argument('order_col', type=str, default='accession_id')
table_parser.add_argument('order_dir', type=str, default='asc')


class ColumnEpi:

    def __init__(self, text, field, description, type, is_numerical=False, is_percentage=False):
        self.text = text
        self.field = field
        self.description = description
        self.type = type
        self.is_numerical = is_numerical
        self.is_percentage = is_percentage

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


columns_epi_sel = [
    ColumnEpi('Protein Name', 'product', 'Name of the protein where the epitopes must be located', 'str', False, False),
    ColumnEpi('Assay', 'cell_type', 'Assay type of the epitopes', 'str', False, False),
    ColumnEpi('HLA restriction', 'mhc_allele', 'HLA restriction that must be related to the epitopes', 'str', False, False),
    ColumnEpi('Is Linear', 'is_linear', 'Information related to the type of the epitopes (linear or conformational)', 'str', False, False),
    ColumnEpi('Response Frequency', 'response_frequency', 'info resp freq', 'num', False, True),
    ColumnEpi('Position Range', 'position_range', 'Range in which the epitopes must have at least a part included', 'num', True, False),
    ColumnEpi('Epitope IEDB ID', 'iedb_epitope_id', 'IEDB ID of the epitope', 'num', False, False),
    #ColumnEpi('Assay Type', 'assay_type', 'Assay type', 'str', False, False),
]

columns_epi_amino = [
    ColumnEpi('Variant Position Range', 'variant_position_range',
              'Range of positions within the amino acid sequence of the gene, based on the reference sequence. '
              'Insertions and deletions have arbitrary lengths. Substitutions only involve one amino acid residue. '
              'Please search for one single substitution at a time.', 'num',
              True, False),
    ColumnEpi('Variant Type', 'variant_aa_type', 'Type of amino acid change that must appear in the epitopes (SUB = substitution, INS = insertion, DEL = deletion)', 'str', False, False),
    ColumnEpi('Original Aminoacid', 'sequence_aa_original', 'Affected amino acid sequence from the corresponding reference sequence of the chosen Virus', 'str', False, False),
    ColumnEpi('Alternative Aminoacid', 'sequence_aa_alternative', 'Changed amino acid sequence (in the target sequence) with respect to the reference one', 'str', False, False),
]

columns_user_new_epi_sel = [
    ColumnEpi('Epitope Name', 'epitope_name', 'Name of the custom epitope (Names must be unique)', 'str', False, False),
    ColumnEpi('Protein Name', 'product', 'Name of the protein where the custom epitope will be located', 'str', False, False),
    ColumnEpi('Position Range', 'position_range', 'Range within the chosen protein in which the custom epitope is located. More than one range could be selected to create a conformational epitope (Add one fragment range at a time)', 'num', True, False),
]

columns_user_new_epi_amino = [
    ColumnEpi('Protein Name', 'product', 'Protein produced by the sub-sequence within which the amino acid change occurs', 'str', False, False),
    ColumnEpi('Position Range', 'position_range', 'Range of positions within the amino acid sequence of the gene, based on the reference sequence', 'num', True, False),
    ColumnEpi('Variant Type', 'variant_aa_type', 'Type of amino acid change (SUB = substitution, INS = insertion, DEL = deletion)', 'str', False, False),
    ColumnEpi('Original Aminoacid', 'sequence_aa_original', 'Affected amino acid sequence from the corresponding reference sequence of the chosen Virus', 'str', False, False),
    ColumnEpi('Alternative Aminoacid', 'sequence_aa_alternative', 'Changed amino acid sequence (in the target sequence) with respect to the reference one', 'str', False, False),
]

columns_dict_epi_sel = {x.field: x for x in columns_epi_sel}

columns_dict_user_new_epi_sel = {x.field: x for x in columns_user_new_epi_sel}

columns_dict_epi_amino = {x.field: x for x in columns_epi_amino}

columns_dict_user_new_epi_amino = {x.field: x for x in columns_user_new_epi_amino}

columns_dict_epi_all = {x.field: x for x in columns_epi_sel + columns_epi_amino}


field = api.model('Field', {
    'text': fields.String(attribute='text', required=True, description='Name of the Field '),
    'field': fields.String(attribute='field', description='Field in table '),
    'description': fields.String(attribute='description', description='Field description '),
    'is_numerical': fields.Boolean(attribute='is_numerical',
                                   description='True if field is numerical, False otherwise '),
    'is_percentage': fields.Boolean(attribute='is_percentage', description='True if field is a percentage'
                                                                           ', False otherwise '),
})

field_list = api.model('Fields', {
    'fields': fields.List(fields.Nested(field, required=True, description='Fields', skip_none=True))
})


########################################################################################################


@api.route('')
class FieldList(Resource):
    @api.doc('get_field_list')
    def get(self):
        res = {'fields': "hello"}
        return res

