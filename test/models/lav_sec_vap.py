# -*- coding: utf-8 -*-

from lxml import etree
from re import compile
from itertools import groupby
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class MaquinasLav(models.Model):
    _name = 'lavanderia.maquina'
    _rec_name = 'denominacion'
    # Campos Comunes
    codigo = fields.Char(string='Código',
                         size=2,
                         required=True)
    denominacion = fields.Char(string='Denominación',
                               size=30,
                               required=True)
    # Restricciones
    _sql_constraints = [('lavadora_unica',
                         'UNIQUE (codigo)',
                         "Ya existe una lavadora con el código escrito")]


class MaquinasSec(models.Model):
    _name = 'lavanderia.secadora'
    _rec_name = 'codigo'
    # Campos Comunes
    codigo = fields.Char(string='Código',
                         size=3,
                         required=True)
    marca = fields.Char(string='Marca',
                        size=30,
                        required=True)

    # Funciones: 'Front-End'
    def name_get(self, cr, uid, ids, context=None):
        res = []
        maquinas = self.browse(cr, uid, ids, context)
        for maquina in maquinas:
            res.append((maquina.id, maquina.codigo + ": " + maquina.marca))
        return res

    # Restricciones
    @api.one
    @api.constrains('codigo')
    def check_code(self):
        if(len(self.codigo) != 3):
            msg = "El campo código debe tener 3 caractéres"
            raise ValidationError(msg)

    _sql_constraints = [('secadora_unica',
                         'UNIQUE (codigo)',
                         "Ya existe una secadora con el código escrito")]


class ProgramaLavSec(models.Model):
    _name = 'lavanderia.programa'
    _rec_name = 'denominacion'
    # Campos Comunes
    codigo = fields.Integer(string='Código',
                            required=True)
    denominacion = fields.Char(string='Denominación',
                               compute='_get_denominacion',
                               store=True)
    colores = fields.Selection([('C', 'Color'),
                                ('B', 'Blanco')],
                               "Para Colores",
                               default='C',
                               required=True)
    medidas = fields.Selection([('E', 'Exactas'),
                                ('G', 'Grandes')],
                               "Para Medidas",
                               default='E',
                               required=True)
    tipo_galga = fields.Selection([('F', 'Fina'),
                                   ('G', 'Gruesa'),
                                   ('T', 'Todas')],
                                  "Tipo de Galga",
                                  default='T',
                                  required=True)
    tipo_obj = fields.Selection([('001', 'Prendas'),
                                 ('010', 'Paneles'),
                                 ('011', 'Paneles y Prendas'),
                                 ('101', 'Prendas con Accesorios'),
                                 ('111', 'Paneles y Prendas con Accesorios')],
                                "Tipo de Objeto",
                                default='001',
                                required=True)
    material = fields.Selection([('G', 'Algodón'),
                                 ('O', 'Oveja'),
                                 ('A', 'Alpaca')],
                                'Material',
                                default='G',
                                required=True)
    temperatura = fields.Integer(string='Temperatura',
                                 required=True)
    cantidad_agua = fields.Integer(string='Cantidad de Agua',
                                   required=True)
    llenado_agua = fields.Float(string='Tiempo de Llenado de Agua',
                                required=True)
    calentado = fields.Float(string='Tiempo de Calentado',
                             required=True)
    lavado = fields.Float(string='Tiempo de Lavado',
                          required=True)
    remojo = fields.Float(string='Tiempo de Remojo',
                          required=True)
    drenado = fields.Float(string='Tiempo de Drenado',
                           required=True)
    centrifugado = fields.Float(string='Tiempo de Centrifugado',
                                required=True)
    t_total = fields.Float(string='Tiempo Total',
                           compute='actualizar_total_tiempo',
                           store=True)
    # Campos Relacionados
    maquina_id = fields.Many2one(
        'lavanderia.maquina',
        'Máquina',
        required=True
    )

    # Funciones: 'Computadas'
    @api.model
    @api.depends('codigo', 'maquina_id')
    def _get_denominacion(self):
        deno = "Programa "+str(self.codigo)+" "
        if(self.maquina_id):
            deno += self.maquina_id.codigo
        self.denominacion = deno

    @api.one
    @api.depends('llenado_agua', 'calentado', 'lavado',
                 'remojo', 'drenado', 'centrifugado')
    def actualizar_total_tiempo(self):
        self.t_total = self.llenado_agua + self.calentado + self.lavado
        self.t_total += self.remojo + self.drenado + self.centrifugado

    # Restricciones
    _sql_constraints = [('programa_unico',
                         'UNIQUE (codigo,maquina_id)',
                         "Ya existe el programa en la máquina seleccionada")]


class Suavizante(models.Model):
    _name = 'lavanderia.suavizante'
    _rec_name = 'denominacion'
    # Campos Comunes
    denominacion = fields.Char(string='Denominación',
                               size=30,
                               required=True)


class Detergente(models.Model):
    _name = 'lavanderia.detergente'
    _rec_name = 'denominacion'
    # Campos Comunes
    denominacion = fields.Char(string='Denominación',
                               size=30,
                               required=True)


class Vapor(models.Model):
    _name = 'vapor.tipo'
    _rec_name = 'denominacion'

    denominacion = fields.Char(string='Denominación',
                               size=30,
                               required=True)
