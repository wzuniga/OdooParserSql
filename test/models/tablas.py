# -*- coding: utf-8 -*-

from re import compile
from itertools import groupby
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class TablaPesos(models.Model):
    _name = 'tejido.tablas.pesos'
    _rec_name = 'matrix_x'
    # Campos Comunes
    matrix_x = fields.Char(string='Panel')
    matrix_y = fields.Char(string='Colores')
    value = fields.Float(string='Valor')
    # Campos Relacionados
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )


class TablaPorcentajes(models.Model):
    _name = 'tejido.tablas.porcentajes'
    _rec_name = 'matrix_x'
    # Campos Comunes
    matrix_x = fields.Char(string='Total %')
    matrix_y = fields.Char(string='Colores')
    value = fields.Float(string='Valor')
    # Campos Relacionados
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )


class TablaTiempos(models.Model):
    _name = 'tejido.tablas.tiempos'
    # Campos Comunes
    nombre_panel = fields.Char(string='Panel',
                               size=30,
                               required=True)
    tiempo_bajada = fields.Float(string='Tiempo Bajada')
    cantidad = fields.Integer(string='Cantidad Paneles')
    tiempo_unitario = fields.Float(string='Tiempo Unitario',
                                   compute='_F_tiempo_unitario',
                                   store=True)
    # Campos Relacionados
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )
    componente_id = fields.Many2one(
        'tejido.componente.panel',
        'Componente',
        ondelete='cascade'
    )

    # Funciones: 'Computadas'
    @api.one
    @api.depends('tiempo_bajada', 'cantidad')
    def _F_tiempo_unitario(self):
        if(self.cantidad > 0):
            self.tiempo_unitario = self.tiempo_bajada/self.cantidad
        else:
            self.tiempo_unitario = 0


class TablaOperaciones(models.Model):
    _name = 'tejido.tablas.operaciones'
    _rec_name = 'header'
    # Campos Comunes
    header = fields.Char(string='Tipo')
    header_2 = fields.Char(string='SubTipo')
    option = fields.Char(string='Estilo')
    selected = fields.Boolean(string='Valor')
    # Campos Relacionados
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )


class TablaGuiaHilos(models.Model):
    _name = 'tejido.tablas.guiahilos'
    _rec_name = 'matrix_x'
    # Campos Comunes
    matrix_x = fields.Char(string='Panel')
    matrix_y = fields.Char(string='Índice Guia Hilo')
    value = fields.Char(string='Valor')
    # Campos Relacionados
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )


class TablaVelocidades(models.Model):
    _name = 'tejido.tablas.velocidad'
    _rec_name = 'nombre'
    # Campos Comunes
    nombre = fields.Char(string='Nombre',
                         size=20)
    velocidad = fields.Float(string='Velocidad')
    # Campos Relacionados
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )


class TablaCodificacionProgramas(models.Model):
    _name = 'tejido.cod.programas'
    _rec_name = 'componente_panel_ids'
    # Campos Comunes
    cantidad = fields.Integer(string='Cantidad',
                              compute='get_data_from_component')
    talla = fields.Char(string='Talla',
                        size=5,
                        required=True)
    # Campos Relacionados
    abrv_id = fields.Many2one(
        'tejido.componente.abreviatura',
        'Abreviatura',
        compute='get_data_from_component'
    )
    componente_panel_ids = fields.Many2one(
        'tejido.componente.panel',
        'Componente',
        required=True,
        ondelete='cascade'
    )
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )

    # Funciones: 'Computadas'
    @api.one
    @api.depends('componente_panel_ids')
    def get_data_from_component(self):
        if(self.componente_panel_ids):
            self.cantidad = self.componente_panel_ids.cantidad
            self.abrv_id = self.componente_panel_ids.componente_abreviatura_id
        else:
            self.cantidad = 0
            self.abrv_id = None


class TablaTecnicoMedidas(models.Model):
    _name = 'tejido.medidas.tecnico'
    _rec_name = 'matrix_x'
    # Campos Comunes
    matrix_x = fields.Char(string='Medidas')
    matrix_y = fields.Char(string='Componentes')
    value = fields.Char(string='Valor')
    # Campos Relacionados
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )
