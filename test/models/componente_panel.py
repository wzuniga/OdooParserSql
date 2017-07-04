# -*- coding: utf-8 -*-

from lxml import etree
from re import compile
from itertools import groupby
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class ComponenteAbreviatura(models.Model):
    _name = 'tejido.componente.abreviatura'
    _rec_name = 'abreviatura'

    abreviatura = fields.Char(string='Abreviatura',
                              size=2,
                              required=True,)
    descripcion = fields.Char(string='Descripción',
                              size=30,
                              required=True,)


class ComponentePanel(models.Model):
    _name = 'tejido.componente.panel'
    _rec_name = 'denominacion'
    # Campos Comunes
    denominacion = fields.Char(string='Descripción',
                               size=30,
                               required=True,)
    cantidad = fields.Integer(string='Cantidad',
                              default=1,
                              required=True)
    cuadro_mallas_agujas = fields.Float(string='CM: Agujas',
                                        required=True,)
    cuadro_mallas_filas = fields.Float(string='CM: Filas',
                                       required=True,)
    ancho_maximo = fields.Float(string='Ancho Máximo',
                                default=0)
    numero_cabos = fields.Integer(string='Número de Cabos',
                                  default=0)
    dificultad = fields.Selection([('A', 'A'),
                                   ('B', 'B'),
                                   ('C', 'C'),
                                   ('D', 'D')],
                                  string="Dificultad",
                                  required=True)
    # Campos Relacionados
    punto_id = fields.Many2one(
        'desarrollo.punto',
        'Punto',
        required=True
    )
    galga_id = fields.Many2one(
        'desarrollo.galga',
        'Galga',
        required=True
    )
    maquina_id = fields.Many2one(
        'desarrollo.maquina',
        'Máquina',
        required=True
    )
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )
    componente_base_id = fields.Many2one(
        'modeloprenda.componente.rel',
        'Componente Base',
        required=True,
        ondelete='cascade'
    )
    componente_abreviatura_id = fields.Many2one(
        'tejido.componente.abreviatura',
        'Abreviatura',
        required=True
    )

    # Funciones: 'On Change'
    @api.model
    @api.onchange('componente_base_id')
    def get_data_from_component(self):
        if(self.componente_base_id):
            componente_base = self.componente_base_id.componente_id
            denominacion = componente_base.descripcion_componente
            self.denominacion = denominacion
            self.punto_id = self.componente_base_id.punto_id
            self.galga_id = self.componente_base_id.galga_id
            self.numero_cabos = self.componente_base_id.numero_cabos
        else:
            self.denominacion = ""
            self.punto_id = None
            self.galga_id = None
            self.numero_cabos = 0

    @api.model
    @api.onchange('maquina_id', 'cuadro_mallas_agujas')
    def get_ancho_maximo(self):
        if(self.cuadro_mallas_agujas != 0 and self.maquina_id):
            self.ancho_maximo = self.maquina_id.numero_agujas
            self.ancho_maximo /= self.cuadro_mallas_agujas

    # Funciones: 'Front-End'
    @api.multi
    def get_machine(self, _galga_id):
        if _galga_id:
            galga = self.env['desarrollo.galga'].browse(_galga_id)
            return {
                'domain': {
                    'maquina_id': [('id', 'in', galga.maquina_ids.ids)],
                },
                'value': {'maquina_id': False}
            }
        else:
            return {
                'domain': {
                    'maquina_id': [('id', '=', 0)],
                },
                'value': {'maquina_id': False}
            }


class ComponenteDatosTejido(models.Model):
    _name = 'tejido.comp.datos'
    # Campos Comunes
    total_tupideses = fields.Integer(string='Total de Tupideses',
                                     compute='get_total_tupideses',
                                     store=True)
    # Campos Relacionados
    maquina_id = fields.Many2one(
        'desarrollo.maquina',
        'Máquina',
        compute='get_data_from_component',
        store=True
    )
    galga_id = fields.Many2one(
        'desarrollo.galga',
        'Galga',
        compute='get_data_from_component',
        store=True
    )
    tupideses_ids = fields.One2many(
        'tejido.tupideses.rel',
        'componente_dato_tejido_id',
        string='Tupideses'
    )
    componente_panel_ids = fields.Many2many(
        'tejido.componente.panel',
        string='Componente',
        ondelete='cascade'
    )
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )

    # Funciones: 'Computadas'
    @api.multi
    @api.depends('tupideses_ids')
    def get_total_tupideses(self):
        for componente in self:
            componente.total_tupideses = len(componente.tupideses_ids)

    @api.one
    @api.depends('componente_panel_ids')
    def get_data_from_component(self):
        check_maquina_id = {}
        check_galga_id = {}
        for componente_panel_id in self.componente_panel_ids:
            self.maquina_id = componente_panel_id.maquina_id
            self.galga_id = componente_panel_id.galga_id
            check_maquina_id[self.maquina_id.id] = 1
            check_galga_id[self.galga_id.id] = 1
        if((len(check_galga_id.keys()) > 1) or
           (len(check_maquina_id.keys()) > 1)):
            msg = "Los componentes no tiene la misma máquina y galga."
            raise ValidationError(msg)

    # Funciones: 'Front-End'
    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        res = super(ComponenteDatosTejido, self).fields_view_get(cr, uid,
                                                                 view_id,
                                                                 view_type,
                                                                 context,
                                                                 toolbar,
                                                                 submenu)
        _file = context.get('var_file_id', 0)
        doc = etree.XML(res['arch'])
        nodes = doc.xpath("//field[@name='componente_panel_ids']")
        for node in nodes:
            node.set('domain',
                     "[('file_seguimiento_id', '=', {0})]".format(_file)
                     )
        res['arch'] = etree.tostring(doc)
        return res

    # Restricciones
    @api.one
    @api.constrains('componente_panel_ids')
    def check_maquinas_y_galgas(self):
        check_maquina_id = {}
        check_galga_id = {}
        for componente_panel_id in self.componente_panel_ids:
            check_maquina_id[componente_panel_id.maquina_id.id] = 1
            check_galga_id[componente_panel_id.galga_id.id] = 1
        if((len(check_galga_id.keys()) > 1) or
           (len(check_maquina_id.keys()) > 1)):
            msg = "Los datos de tejido tienen componentes"\
                  " que no tienen la misma máquina y galga."
            raise ValidationError(msg)


class VariableTupideses(models.Model):
    _name = 'tejido.var.tup'
    _rec_name = 'detalle'
    # Campos Comunes
    detalle = fields.Char(string='Detalle',
                          size=30,
                          required=True)
    cantidad = fields.Integer(string='Cantidad')
    knit_in_agu = fields.Float(string='Knit In: Agujas')
    knit_in_var = fields.Float(string='Knit In: Variable')
    knit_out_agu = fields.Float(string='Knit Out: Agujas')
    knit_out_var = fields.Float(string='Knit Out: Variable')
    # Campos Relacionados
    componente_panel_ids = fields.Many2one(
        'tejido.componente.panel',
        'Componente',
        required=True,
        ondelete='cascade'
    )
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento'
    )


class CompParametrosTejido(models.Model):
    _name = 'tejido.comp.param'
    # Campos Comunes
    total_pruebas = fields.Integer(string='Total de Pruebas',
                                   compute='get_total_pruebas',
                                   store=True)
    # Campos Relacionados
    maquina_id = fields.Many2one(
        'desarrollo.maquina',
        'Máquina',
        compute='get_data_from_component',
        store=True
    )
    galga_id = fields.Many2one(
        'desarrollo.galga',
        'Galga',
        compute='get_data_from_component',
        store=True
    )
    pruebas_ids = fields.One2many(
        'tejido.estiraje.rel',
        'componente_parametro_tejido_id',
        string='Pruebas de Estiraje'
    )
    componente_panel_ids = fields.Many2one(
        'tejido.componente.panel',
        'Componente',
        ondelete='cascade'
    )
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )

    # Funciones: 'Computadas'
    @api.multi
    @api.depends('pruebas_ids')
    def get_total_pruebas(self):
        for componente in self:
            componente.total_pruebas = len(componente.pruebas_ids)

    @api.one
    @api.depends('componente_panel_ids')
    def get_data_from_component(self):
        if(self.componente_panel_ids):
            self.maquina_id = self.componente_panel_ids.maquina_id
            self.galga_id = self.componente_panel_ids.galga_id
        else:
            self.maquina_id = None
            self.galga_id = None

    # Funciones: 'Front-End'
    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        res = super(CompParametrosTejido, self).fields_view_get(cr, uid,
                                                                view_id,
                                                                view_type,
                                                                context,
                                                                toolbar,
                                                                submenu)
        _file = context.get('var_file_id', 0)
        doc = etree.XML(res['arch'])
        nodes = doc.xpath("//field[@name='componente_panel_ids']")
        for node in nodes:
            node.set('domain',
                     "[('file_seguimiento_id', '=', {0})]".format(_file)
                     )
        res['arch'] = etree.tostring(doc)
        return res


class CompTecnicoRelacion(models.Model):
    _name = 'tej.tecn.comp'
    # Campos Comunes
    peso = fields.Float(string='Peso (Kg)',
                        required=True,
                        digits=(13, 3))
    observacion = fields.Text(string='Observación')
    cantidad = fields.Integer(string='Cantidad',
                              default=1,
                              required=True)
    # Campos Relacionados
    componente_panel_ids = fields.Many2one(
        'tejido.componente.panel',
        'Componente',
        ondelete='cascade'
    )
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )
