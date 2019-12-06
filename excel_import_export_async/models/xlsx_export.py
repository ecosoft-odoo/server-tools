# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, api


class XLSXExport(models.AbstractModel):
    _inherit = 'xlsx.export'

    @api.model
    def export_xlsx(self, template, res_model, res_id):
        """Delay export if specified"""
        if not self._context.get('async_process', False):
            return super().export_xlsx(template, res_model, res_id)
        self.env['delay.export'].with_delay().\
            export_xlsx(template, res_model, res_id,
                        user_ids=[self._uid])
        return (False, False)
