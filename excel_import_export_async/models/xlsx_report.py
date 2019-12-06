# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, fields, api


class XLSXReport(models.AbstractModel):
    _inherit = 'xlsx.report'

    async_process = fields.Boolean(
        string='Asynchronous',
        default=False,
    )

    @api.multi
    def report_xlsx(self):
        ctx = {'async_process': self.async_process}
        return super(XLSXReport, self.with_context(ctx)).report_xlsx()
