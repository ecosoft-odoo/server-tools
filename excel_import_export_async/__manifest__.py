# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'Excel Import/Export Async',
    'summary': """
        Asynchronous excel export with job queue
    """,
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/queue',
    'depends': [
        'excel_import_export',
        'base_export_async',
    ],
    'data': [
        'views/xlsx_report.xml',
    ],
    'demo': [
    ],
}
