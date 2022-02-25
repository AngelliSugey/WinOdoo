# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'open_academy.wizard'
    _description = 'Sesion'

    def _default_session(self):
        return self.env['open_academy.sesion'].browse(self._context.get('active_id'))

    sesion_id = fields.Many2one('open_academy.sesion', string="Sesion", required=True, default=_default_session)
    assistants_id = fields.Many2many('res.partner', string="Attendees")

    def agregar(self):
        self.sesion_id.assistants_id |= self.assistants_id
        return{}