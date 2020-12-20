# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
import datetime

class SaleOrderLine(models.Model):
    _inherit ='sale.order.line'

    consignment_id = fields.Integer(string='ID Consignatorio', compute='_consig_ID')

    def _consig_ID(self):
        self.consignment_id = self.product_id.consignment.consignment_id


class SaleOrder(models.Model):
    _inherit ='sale.order'
    date_report = fields.Date(string='Fecha de Nacimiento', compute='_date_format_report')

    def _date_format_report(self):
        try:
            self.date_report = self.date_order.date()
        except:
            self.date_report = datetime.datetime.now().date()

    def send_report_daily(self):

        docids = self.env['sale.order'].search([('invoice_status', '=', 'invoiced'),('date_report','=', datetime.datetime.now().date())])

        if len(docids) > 0:
            return self.env.ref('prueba_vicom.sale_summary_report').report_action(docids)
        else:
            pass
