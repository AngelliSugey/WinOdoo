# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'open_academy.wizard'
    _description = 'Sesion'

    def _default_session(self):
        return self.env['open_academy.sesion'].browse(self._context.get('active_id'))

    id_sesion = fields.Many2one('open_academy.sesion', string="Sesion", required=True, default=_default_session)
    id_assistants = fields.Many2many('res.partner', string="Attendees")

    def agregar(self):
        for sesion in self.id_sesion:
            sesion.id_assistants |= self.id_assistants
        return{}