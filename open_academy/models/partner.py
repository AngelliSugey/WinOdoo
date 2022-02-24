# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)

    id_sesions = fields.Many2many('open_academy.sesion', string="Sesiones Asistidas", readonly=True)