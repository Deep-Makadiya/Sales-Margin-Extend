from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_margin = fields.Float(string='Product Margin')

