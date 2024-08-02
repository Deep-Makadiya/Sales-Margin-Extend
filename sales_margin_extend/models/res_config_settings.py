from odoo import models, fields, api, _


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    product_margin = fields.Float(string='Product Margin')

    def set_values(self):
        super(ResConfigSetting, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sales_margin_extend.product_margin', self.product_margin)

    @api.model
    def get_values(self):
        res = super(ResConfigSetting, self).get_values()
        res['product_margin'] = float(
            self.env['ir.config_parameter'].sudo().get_param('sales_margin_extend.product_margin', default=0.0))
        return res
