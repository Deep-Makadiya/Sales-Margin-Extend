from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        if self.product_id:
            product_margin = 0.0

            # Check product margin in product
            if self.product_id.product_tmpl_id and self.product_id.product_tmpl_id.product_margin:
                product_margin = self.product_id.product_tmpl_id.product_margin
                print("Product value >>>>>>>", product_margin)
            # Check product margin in product category
            elif self.product_id.categ_id and self.product_id.categ_id.product_margin:
                product_margin = self.product_id.categ_id.product_margin
                print("Product categories value>>>>>>>>>>", product_margin)
            # Check product margin in configure setting
            else:
                product_margin = float(
                    self.env['ir.config_parameter'].sudo().get_param('sales_margin_extend.product_margin',
                                                                     default=0.0))
                print("Product setting value>>>>>>>>>>>>>>>>", product_margin)

            self.price_unit += self.price_unit * (product_margin / 100.0)
