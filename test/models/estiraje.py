# -*- coding: utf-8 -*-

from re import compile
from itertools import groupby
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class EstirajeRelacion(models.Model):
    _name = 'tejido.estiraje.rel'
    # Campos Comunes
    talla = fields.Char(string='Talla',
                        size=5,
                        required=True)
    peso = fields.Char(string='Peso Utilizado kg',
                       required=True)
    value = fields.Float(string='Valor',
                         required=True)
    # Campos Relacionados
    componente_parametro_tejido_id = fields.Many2one(
        'tejido.comp.param',
        'Parámetros Componente',
        ondelete='cascade'
    )


class EstirajeCuadroMalla(models.Model):
    _name = 'tejido.est.malla'
    # Campos Comunes
    numero_de_puntos = fields.Float(string='Total de Puntos',
                                    required=True)
    distancia = fields.Float(string='Distancia (mm)',
                             required=True)
    # Campos Relacionados
    punto_id = fields.Many2one(
        'desarrollo.punto',
        'Punto',
        store=True,
        required=True
    )
    galga_id = fields.Many2one(
        'desarrollo.galga',
        'Galga',
        store=True,
        required=True
    )
    componente_panel_ids = fields.Many2one(
        'tejido.componente.panel',
        'Componente Relacionado',
        ondelete='cascade'
    )
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )

    # Funciones: 'On Change'
    @api.model
    @api.onchange('componente_panel_ids')
    def get_data_from_component(self):
        if(self.componente_panel_ids):
            self.galga_id = self.componente_panel_ids.galga_id
            self.punto_id = self.componente_panel_ids.punto_id
        else:
            self.galga_id = None
            self.punto_id = None


class EstirajeMedidasSeco(models.Model):
    _name = 'tejido.est.seco'
    # Campos Comunes
    detalle = fields.Char(string='Detalle',
                          size=30)
    medida = fields.Float(string='Medida al Seco (cm)',
                          required=True)
    observacion = fields.Text(string='Observación')
    # Campos Relacionados
    galga_id = fields.Many2one(
        'desarrollo.galga',
        'Galga',
        store=True,
        required=True
    )
    componente_panel_ids = fields.Many2one(
        'tejido.componente.panel',
        'Componente Relacionado',
        ondelete='cascade'
    )
    file_seguimiento_id = fields.Many2one(
        'tejido.file.seguimiento',
        'File de Seguimiento',
        ondelete='cascade'
    )

    # Funciones: 'On Change'
    @api.model
    @api.onchange('componente_panel_ids')
    def get_data_from_component(self):
        if(self.componente_panel_ids):
            self.galga_id = self.componente_panel_ids.galga_id
        else:
            self.galga_id = None
