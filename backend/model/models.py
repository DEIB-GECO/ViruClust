# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Integer, Table, Text, UniqueConstraint

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# t_flatten = db.Table(
#     'flatten',
#     db.Column('item_id', db.Integer),
#     db.Column('item_source_id', db.Text),
#     db.Column('alt_item_source_id', db.Text),
#     db.Column('biosample_type', db.Text),
#     db.Column('tissue', db.Text),
#     db.Column('cell', db.Text),
#     db.Column('is_healthy', db.Boolean),
#     db.Column('disease', db.Text),
#     db.Column('biosample_source_id', db.Text),
#     db.Column('alt_biosample_source_id', db.Text),
#     db.Column('source_site', db.Text),
#     db.Column('external_reference', db.Text),
#     db.Column('dataset_name', db.Text),
#     db.Column('data_type', db.Text),
#     db.Column('file_format', db.Text),
#     db.Column('assembly', db.Text),
#     db.Column('is_annotation', db.Boolean),
#     db.Column('species', db.Text),
#     db.Column('age', db.Integer),
#     db.Column('gender', db.Text),
#     db.Column('ethnicity', db.Text),
#     db.Column('donor_source_id', db.Text),
#     db.Column('alt_donor_source_id', db.Text),
#     db.Column('technique', db.Text),
#     db.Column('feature', db.Text),
#     db.Column('target', db.Text),
#     db.Column('antibody', db.Text),
#     db.Column('platform', db.Text),
#     db.Column('pipeline', db.Text),
#     db.Column('content_type', db.Text),
#     db.Column('source', db.Text),
#     db.Column('project_name', db.Text),
#     db.Column('biological_replicate_number', db.Integer),
#     db.Column('technical_replicate_number', db.Text),
#     db.Column('biological_replicate_count', db.BigInteger),
#     db.Column('technical_replicate_count', db.BigInteger),
#     db.UniqueConstraint('item_id', 'biosample_type', 'tissue', 'cell', 'is_healthy', 'disease', 'biosample_source_id',
#                         'source_site', 'external_reference', 'dataset_name', 'data_type', 'file_format', 'assembly',
#                         'is_annotation', 'species', 'age', 'gender', 'ethnicity', 'donor_source_id', 'technique',
#                         'feature', 'target', 'antibody', 'platform', 'pipeline', 'content_type', 'source',
#                         'project_name', 'biological_replicate_number', 'technical_replicate_number',
#                         'biological_replicate_count', 'technical_replicate_count'),
#     schema='dw'
# )
