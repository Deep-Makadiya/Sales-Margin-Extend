from odoo import models, fields, api, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    product_margin = fields.Float(string='Product Margin')
