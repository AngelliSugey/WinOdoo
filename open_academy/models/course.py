# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'Course'

    title = fields.Char(string="Title", required=True)
    description = fields.Text()

    id_responsable = fields.Many2one('res.users', ondelete='set null', string="Responsable", index=True)
    id_sesion = fields.One2many('open_academy.sesion', 'id_course', string="Sesions")


    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('title', '=like', _(u"Copy of {}%").format(self.title))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.title)
        else:
            new_name = _(u"Copy of {} ({})").format(self.title, copied_count)
        
        default['title'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(title != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(title)',
         "The course title must be unique"),
    ]

class Sesion(models.Model):
    _name = 'open_academy.sesion'
    _description = 'Sesion'

    title = fields.Char(string="Title", required=True)
    date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(8, 2), help="Duracion en dias")
    seats = fields.Integer(string="Numero de Asiento")
    active = fields.Boolean(default=True)
    color = fields.Integer()

    id_instructor = fields.Many2one('res.partner', string="Instructor", domain=[('instructor', '=', True), ('category_id.name', 'ilike', "Teacher") ])
    id_course = fields.Many2one('open_academy.course', ondelete='cascade', string="Course", required=True)
    id_assistants = fields.Many2many('res.partner', string="Asistentes")

    t_seats = fields.Float(string="Taken Seats", compute='_taken_seats')

    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string="Duration in hours", compute='_get_hours', inverse='_set_hours') 

    assistants_count = fields.Integer(string="Assistants Count", compute='_get_attendees_count', store=True)

    @api.depends('seats', 'id_assistants')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.t_seats = 00
            else:
                r.t_seats = 100.0 * len(r.id_assistants) / r.seats
    
    @api.onchange('seats', 'id_assistants')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of avaliable seats may not be negative"),
                },
            }
        if self.seats < len(self.id_assistants):
            return {
                'warning': {
                    'title': _("Too many assistants"),
                    'message': _("Increase seats or remove excess assistants"),
                },
            }

    @api.depends('date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.date and r.duration):
                r.end_date = r.date
                continue

            start = fields.Datetime.from_string(r.date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.date and r.end_date):
                continue

            start_date = fields.Datetime.from_string(r.date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24
    
    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24
    

    @api.depends('id_assistants')
    def _get_attendees_count(self):
        for r in self:
            r.assistants_count = len(r.id_assistants)

    @api.constrains('id_instructor', 'id_assistants')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.id_instructor and r. id_instructor in r.id_assistants:
                raise exceptions.ValidationError(_("A session's instructor can't be an assistants"))

