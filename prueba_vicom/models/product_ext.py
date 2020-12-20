# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
import random

class ProductExt(models.Model):
    _inherit ='product.product'

    consignment = fields.Many2one('res.partner', string='Consignatario', required=True, compute='_product_temp', domain=[('consignment', '=', True)])
    marca = fields.Char('Marca', required=True, compute='_product_temp')
    modelo = fields.Char('Modelo', required=True, compute='_product_temp')

    @api.model
    def _product_temp(self):
        self.consignment = self.product_tmpl_id[0].consignment
        self.marca = self.product_tmpl_id[0].marca
        self.modelo = self.product_tmpl_id[0].modelo

    @api.model
    def create(self, vals):
        res = super(ProductExt, self).create(vals)
        ref = res.marca+'-'+res.modelo+'-'+str(res.consignment.consignment_id)
        res.default_code = ref
        productos = self.env['product.product'].search([])
        ready = False
        while not ready:
            num = int(random.random()*100000000)
            ready = True
            for i in productos:
                if str(num) == i.barcode:
                    ready = False


        res.barcode = str(num)

        return res

class ProductTExt(models.Model):
    _inherit ='product.template'

    consignment = fields.Many2one('res.partner', string='Consignatario', required=True, domain=[('consignment', '=', True)])
    marca = fields.Char('Marca', required=True)
    modelo = fields.Char('Modelo', required=True)