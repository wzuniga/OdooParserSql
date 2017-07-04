# -*- coding: utf-8 -*-

from re import compile
from itertools import groupby

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class Usuario(models.Model):
    _inherit = 'res.partner'
    programador = fields.Boolean(string='Programador(a)',
                                 default=False,)
    inspector = fields.Boolean(string='Inspector(a)',
                               default=False,)
    lavanderia = fields.Boolean(string='Personal de Lavandería',
                                default=False,)


class file_seguimiento_material_rel(models.Model):
    _inherit = 'modeloprenda.material.rel'
    file_seguimiento_id = fields.Many2one('tejido.file.seguimiento',
                                          'File de Seguimiento',)


class file_seguimiento_maquina(models.Model):
    _inherit = 'desarrollo.maquina'
    numero_guia_hilos = fields.Integer(string='Número Guia Hilos')
