# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import timedelta

# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
        'res.users', ondelete='set null', string="Resposible", index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Session"
    )


    #self defined copy of records;
    #since the default copy_method was not in function
    #after add the constaints in the model
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))]
        )
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)
        
        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constaints = [
        ('name_description_check',
         'CHECK(name != description)'
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

"""
A course has a responsible user; the value of that field is a record of the built-in model res.users.
A session has an instructor; the value of that field is a record of the built-in model res.partner.
A session is related to a course; the value of that field is a record of the model openacademy.course and is required.
"""





class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6,2), help="Duration in days", default=0)
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
    color = fields.Integer()

    instructor_id = fields.Many2one(
        'res.partner', string="Instructor",
        domain = ['|', ('instructor', '=', True),
                       ('category_id.name', 'ilike', "Teacher")]
    )

    course_id = fields.Many2one(
        'openacademy.course', ondelete='cascade', string="Course", required=True
    )

    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    end_date = fields.Date(string="End date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')

    hours = fields.Float(string="duration in hours", store=True,
                         compute='_get_hours', inverse='_set_hours')

    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True
    )

    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ], default='draft')



    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'




    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0 :
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title':"Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }


    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but Monday+5days =Saturday, so
                # substract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
# it works as not as wanted
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1


    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 10           # 10 hours for a day's session

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 10           # 10 hours for a day's session

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be a an attendee")