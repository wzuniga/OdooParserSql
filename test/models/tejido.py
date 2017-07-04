# -*- coding: utf-8 -*-

from re import compile
from itertools import groupby
from openerp import models, fields, api
from openerp.exceptions import ValidationError
import sapdata


class PartesTejido(models.Model):
    _name = 'tejido.partes'
    _rec_name = 'denominacion'
    # Campos Comunes
    tipo_parte = fields.Selection([('Cuerpo', 'Cuerpo'),
                                   ('Manga', 'Manga'),
                                   ('Swatch', 'Swatch'),
                                   ('Otros', 'Otros')],
                                  "Parte",
                                  default='Cuerpo',
                                  required=True)
    tipo_prenda = fields.Selection(sapdata.get_tprenda().items(),
                                   string='Tipo Prenda',
                                   required=True)
    denominacion = fields.Char(string='Denominación',
                               size=30,
                               required=True)
    # Campos Relacionados
    operaciones_ids = fields.Many2many(
        'tejido.operacion',
        string='Operaciones'
    )

    # Funciones: 'Front-End'
    def name_get(self, cr, uid, ids, context=None):
        res = []
        partes = self.browse(cr, uid, ids, context)
        for parte in partes:
            new_name = parte.tipo_prenda + "-" + parte.tipo_parte + ': '
            new_name += parte.denominacion
            res.append((parte.id, new_name))
        return res

    # Restricciones
    _sql_constraints = [('parte_unica',
                         'UNIQUE (tipo_parte, tipo_prenda, denominacion)',
                         'Esta parte de tejido ya fue ingresada')]


class OperacionTejido(models.Model):
    _name = 'tejido.operacion'
    _rec_name = 'denominacion'
    # Campos Comunes
    denominacion = fields.Char(string='Denominación',
                               size=40,
                               required=True)
    # Campos Relacionados
    parte_ids = fields.Many2many(
        'tejido.partes',
        string='Partes'
    )
    # Restricciones
    _sql_constraints = [('operacion_unica',
                         'UNIQUE (denominacion)',
                         'Esta operacion ya fue ingresada')]
