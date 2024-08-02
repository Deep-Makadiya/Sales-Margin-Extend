from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for invoice in self:
            for line in invoice.invoice_line_ids:
                self._update_product_template_sell_price(line)
        return res

    def _update_product_template_sell_price(self, invoice_line):
        product = invoice_line.product_id.product_tmpl_id
        product_margin = 0.0
        if product and product.product_margin:
            product_margin = product.product_margin
        elif product.categ_id and product.categ_id.product_margin:
            product_margin = product.categ_id.product_margin
        else:
            product_margin = float(
                self.env['ir.config_parameter'].sudo().get_param('sales_margin_extend.product_margin',
                                                                 default=0.0))

        current_margin = ((product.list_price - product.standard_price) / product.standard_price) * 100
        if current_margin < product_margin:
            new_list_price = product.list_price + (product.list_price * product_margin) / 100
            product.write({'list_price': new_list_price})
            product.write({'standard_price': invoice_line.price_unit})
            for seller in product.seller_ids:
                if seller.partner_id.id == self.partner_id.id:
                    seller.write({'price': invoice_line.price_unit})