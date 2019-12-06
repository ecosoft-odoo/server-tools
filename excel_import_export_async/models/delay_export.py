# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _
from odoo.addons.queue_job.job import job


class DelayExport(models.Model):
    _inherit = 'delay.export'

    @api.model
    @job
    def export_xlsx(self, template, res_model, res_id, user_ids=[]):
        """Delayed export of a file sent by email"""
        out_file, out_name = self.env['xlsx.export'].export_xlsx(template,
                                                                 res_model,
                                                                 res_id)
        users = self.env['res.users'].browse(user_ids)
        export_record = self.sudo().create({'user_ids': [(6, 0, users.ids)]})

        attachment = self.env['ir.attachment'].create({
            'name': out_name,
            'datas': out_file,
            'datas_fname': out_name,
            'type': 'binary',
            'res_model': self._name,
            'res_id': export_record.id,
        })

        url = "{}/web/content/ir.attachment/{}/datas/{}?download=true".format(
            self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            attachment.id,
            attachment.name,
        )

        time_to_live = self.env['ir.config_parameter'].sudo().\
            get_param('attachment.ttl', 7)
        date_today = fields.Date.today()
        expiration_date = fields.Date.to_string(
            date_today + relativedelta(days=+int(time_to_live)))

        # TODO: move to email template
        odoo_bot = self.sudo().env.ref("base.partner_root")
        email_from = odoo_bot.email
        description = out_name
        self.env['mail.mail'].create({
            'email_from': email_from,
            'reply_to': email_from,
            'recipient_ids': [(6, 0, users.mapped('partner_id').ids)],
            'subject': _("Export {} {}").format(
                description, fields.Date.to_string(fields.Date.today())),
            'body_html': _("""
                <p>Your excel export is available <a href="{}">here</a>.</p>
                <p>It will be automatically deleted the {}.</p>
                <p>&nbsp;</p>
                <p><span style="color: #808080;">
                This is an automated message please do not reply.
                </span></p>
                """).format(url, expiration_date),
            'auto_delete': True,
        })
