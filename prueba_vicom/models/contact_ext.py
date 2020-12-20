# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class Contacts(models.Model):
    _inherit ='res.partner'

    consignment = fields.Boolean('Es Consignatorio', default=False)
    consignment_id = fields.Integer(string='ID Consignatorio', domain=[('consignment', '=', '1')])
    birthdate = fields.Date(string='Fecha de Nacimiento', required=True, default=fields.datetime.now().date())
    age_num = fields.Integer(compute='_age_num', string='Edad')
    products = fields.One2many('product.product', 'consignment', string='Productos', domain=[('consignment', '=', '1')])
    sex = fields.Selection([('M', 'Masculino'),
                             ('F', 'Femenino'),
                             ('O', 'Otro')], string='Sexo', required=True)


    @api.model
    def _age_num(self):
        if self.birthdate:
            edad = (fields.datetime.now().date() - self.birthdate).days / 365
            if edad < 0:
                edad = 0
            self.age_num = edad
        else:
            pass


    @api.model
    def create(self, vals):
        res = super(Contacts, self).create(vals)
        contactos = self.env['res.partner'].search([('consignment', '=', True)])
        num = 0
        if res.consignment:
            for i in contactos:
                if i.consignment_id >= num:
                    num = i.consignment_id +1
        res.consignment_id = num
        return res

