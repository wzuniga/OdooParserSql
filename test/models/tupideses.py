# -*- coding: utf-8 -*-

from re import compile
from itertools import groupby
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class Tupideses(models.Model):
    _name = 'tejido.tupideses'
    _rec_name = 'denominacion'
    # Campos Comunes
    codigo = fields.Integer(string='Codigo')
    tipo_tupides = fields.Selection([('C', 'Tejido Cuerpo'),
                                     ('P', 'Pretina'),
                                     ('D', 'Dralon')],
                                    "Tipo",
                                    default='C')
    denominacion = fields.Char(string='Denominación',
                               size=30,
                               required=True)

    # Restricciones
    _sql_constraints = [('tupides_unica',
                         'UNIQUE (tipo_tupides,denominacion)',
                         'Esta tupides ya fue ingresada'),
                        ('codigo_unico',
                         'UNIQUE (codigo)',
                         'El codigo ya esta siendo utilizado')]


class TupidesesRelacion(models.Model):
    _name = 'tejido.tupideses.rel'
    # Campos Comunes
    f_value = fields.Integer(string='F',)
    b_value = fields.Integer(string='B',)
    # Campos Relacionados
    tupides_id = fields.Many2one(
        'tejido.tupideses',
        'Detalle'
    )
    componente_dato_tejido_id = fields.Many2one(
        'tejido.comp.datos',
        'Datos Componente',
        ondelete='cascade'
    )
