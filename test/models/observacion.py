# -*- coding: utf-8 -*-

from re import compile
from itertools import groupby
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class Observacion(models.Model):
    _name = 'tejido.file.seguimiento.observaciones'
    # Campos Comunes
    observaciones = fields.Text(string="Observacion")
    # Campos Relacionados
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )
