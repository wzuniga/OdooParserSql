# -*- coding: utf-8 -*-

from re import compile
from itertools import groupby
from openerp import models, fields, api
from openerp.exceptions import ValidationError

file_status = [('Ini', 'Inicio'),
               ('Pre', 'Preparación de Máquinas'),
               ('Par', 'Parámetros de Tejido'),
               ('Lav', 'Control y Lavandería'),
               ('RemAca', 'Confección y Acabado'),
               ('AcaFin', 'Acabado y Control Final'),
               ('Fin', 'Fin')]


class FileSeguimiento(models.Model):
    _name = 'tejido.file.seguimiento'
    _rec_name = 'modelo_prenda_id'
    # Inicio
    estado = fields.Selection(file_status,
                              "Status",
                              default='Ini')
    order_venta = fields.Char(string='Orden de Venta',
                              size=10,
                              required=True)
    tipo_tejido = fields.Selection([('T', 'Tejido'),
                                    ('M', 'Mixto')],
                                   "Tipo Tejido",
                                   default='T',
                                   required=True)
    tipo_operacion = fields.Selection([('Q', 'Máquina'),
                                       ('M', 'Manual')],
                                      "Operación Tejido",
                                      default='Q',
                                      required=True)
    modelo_prenda_id = fields.Many2one(
        'desarrollo.modelo.prenda',
        'Código Modelo',
        required=True
    )
    codigo_modelo_sap = fields.Char(string='Código Modelo SAP',
                                    compute='get_data_from_modelo_prenda',
                                    store=True)
    restricciones = fields.Text(string="Restricciones")
    talla_base = fields.Char(string='Talla Base',
                             size=5,
                             required=True)
    material_ids = fields.One2many(
        'modeloprenda.material.rel',
        'file_seguimiento_id',
        string='Materiales',
        compute='get_data_from_modelo_prenda',
        store=True
    )
    componentes_paneles_ids = fields.One2many(
        'tejido.componente.panel',
        'file_seguimiento_id'
    )
    tabla_pesos = fields.One2many(
        'tejido.tablas.pesos',
        'file_seguimiento_id',
        string='Tabla de Pesos'
    )
    tabla_porcentajes = fields.One2many(
        'tejido.tablas.porcentajes',
        'file_seguimiento_id',
        string='Tabla de Porcentajes'
    )
    tabla_operaciones = fields.One2many(
        'tejido.tablas.operaciones',
        'file_seguimiento_id',
        string='Tipo de Tejido'
    )
    tabla_tiempos = fields.One2many(
        'tejido.tablas.tiempos',
        'file_seguimiento_id',
        string='Tabla de Tiempos'
    )
    tiempo_prenda = fields.Float(string='Tiempo Prenda',
                                 compute='actualizar_total_tiempo',
                                 store=True)
    observaciones_id = fields.One2many(
        'tejido.file.seguimiento.observaciones',
        'file_seguimiento_id',
        string='Observaciones'
    )
    # Preparación de Máquinas
    programador_id = fields.Many2one(
        'res.partner',
        string="Programa Realizado Por",
        domain=['&', ('programador', '=', True)]
    )
    tejedor_id = fields.Many2one(
        'res.partner',
        string="Tejido Por",
        domain=['&', ('programador', '=', True)]
    )
    datos_componentes_ids = fields.One2many(
        'tejido.comp.datos',
        'file_seguimiento_id',
        string='Tupideses'
    )
    variable_tupides_ids = fields.One2many(
        'tejido.var.tup',
        'file_seguimiento_id',
        string='Variable de Tupides'
    )
    velocidad_alta = fields.Float(string='Velocidad Alta',
                                  default=80)
    velocidad_media = fields.Float(string='Velocidad Media',
                                   default=65)
    velocidad_baja = fields.Float(string='Velocidad Baja',
                                  default=45)
    velocidad_en_vacio = fields.Float(string='Pasada En Vacio',
                                      default=1)
    strock = fields.Integer(string='Strock')
    tabla_velocidades = fields.One2many(
        'tejido.tablas.velocidad',
        'file_seguimiento_id',
        string='Otras Velocidades'
    )
    tabla_guia_hilos = fields.One2many(
        'tejido.tablas.guiahilos',
        'file_seguimiento_id',
        string='Guia Hilos'
    )
    tabla_codificacion = fields.One2many(
        'tejido.cod.programas',
        'file_seguimiento_id',
        string='Codificación de Programas'
    )
    # Parámetros de Tejido
    tension_id = fields.Many2one(
        'res.partner',
        string="Tensión Aprobada Por",
        domain=['&', ('programador', '=', True)]
    )
    fecha_pase_control_tecnico = fields.Date(
        string="Fecha Pase Control Técnico"
    )
    parametros_componentes_ids = fields.One2many(
        'tejido.comp.param',
        'file_seguimiento_id',
        string='Estiraje'
    )
    cuadro_mallas_comp_puntos = fields.One2many(
        'tejido.est.malla',
        'file_seguimiento_id',
        string='Cuadro de Mallas'
    )
    medidas_seco_comp = fields.One2many(
        'tejido.est.seco',
        'file_seguimiento_id',
        string='Medidas al Seco'
    )
    # Control y Lavandería
    inspector_control_tecnico_id = fields.Many2one(
        'res.partner',
        string="Inspector(a) Control Técnico",
        domain=['&', ('inspector', '=', True)]
    )
    fecha_pase_lavanderia = fields.Date(string="Fecha Pase Lavandería")
    tabla_control_tecnico = fields.One2many(
        'tejido.medidas.tecnico',
        'file_seguimiento_id',
        string='Control Técnico'
    )
    control_tecnico_pesos_y_observaciones = fields.One2many(
        'tej.tecn.comp',
        'file_seguimiento_id',
        string='Pesos y Observaciones'
    )
    encargado_lavado_id = fields.Many2one(
        'res.partner',
        string="Encargado(a) del Lavado",
        domain=['&', ('lavanderia', '=', True)]
    )
    tipo_lavado = fields.Selection([('A', 'Agua'),
                                    ('S', 'Seco')],
                                   "Tipo de Lavado",
                                   default='A')
    lavado_separado = fields.Boolean(string="Lavado por Separado")
    programa_id = fields.Many2one(
        'lavanderia.programa',
        string="Programa"
    )
    peso_carga = fields.Float(string="Peso (Kg)",
                              digits=(13, 3))
    suavizante_id = fields.Many2one(
        'lavanderia.suavizante',
        string="Suavizante"
    )
    cantidad_suavizante = fields.Float(string="Cantidad Suavizante")
    detergente_id = fields.Many2one(
        'lavanderia.detergente',
        string="Detergente"
    )
    cantidad_detergente = fields.Float(string="Cantidad Detergente")
    encargado_secado_id = fields.Many2one(
        'res.partner',
        string="Encargado(a) del Secado",
        domain=['&', ('lavanderia', '=', True)]
    )
    maquina_secado_id = fields.Many2one(
        'lavanderia.secadora',
        string="Máquina"
    )
    tiempo_secado = fields.Float(string='Tiempo de Secado')
    fecha_pase_control_lavado = fields.Date(
        string="Fecha Pase Control Lavado"
    )
    #vapor
    tipo_vapor_id = fields.Many2one(
        'vapor.tipo',
        'Tipo de Vapor'
    )
    vapor_panel = fields.Boolean(string='Vapor Panel',
                                 help='Tiene o no Vapor en el Panel')
    material_vapor = fields.Char(string='Material',
                                 size=30)
    color_vapor = fields.Char(string='Color',
                              size=30)
    #control lavanderia
    inspector_control_lavado_id = fields.Many2one(
        'res.partner',
        string="Inspector(a) Control Lavado",
        domain=['&', ('inspector', '=', True)]
    )
    fecha_pase_corte = fields.Date(string="Fecha Pase Corte")
    # Confección y Acabado
    observaciones_corte = fields.Text(string="Observaciones Generales Corte")
    fecha_pase_confeccion = fields.Date(string="Fecha Pase Confección")
    fecha_recepcion_costura = fields.Date(string="Fecha Recepción Costura")
    peso_muestra_costura = fields.Float(string="Peso (Kg)")
    fecha_pase_acabado_confeccion = fields.Date(
        string="Fecha Pase Acabado Confección"
    )
    fecha_recepcion_acabado = fields.Date(string="Fecha Recepción Acabado")
    observaciones_acabado = fields.Text(string="Observaciones Acabado")
    peso_muestra_acabado = fields.Float(string="Peso (Kg)")
    fecha_pase_control_confeccion = fields.Date(
        string="Fecha Pase Control de Confección"
    )
    inspector_control_confeccion_id = fields.Many2one(
        'res.partner',
        string="Inspector(a) Control Confección",
        domain=['&', ('inspector', '=', True)]
    )
    observaciones_control_confeccion = fields.Text(
        string="Observaciones Control de Confección"
    )
    fecha_pase_acabado_final = fields.Date(string="Fecha Pase Acabado Final")
    # Acabado Control Final
    fecha_planchado_presentacion = fields.Date(
        string="Fecha de Planchado para Presentación"
    )
    fecha_control_final = fields.Date(string="Fecha de Control Final")
    inspector_arreglos_id = fields.Many2one(
        'res.partner',
        string="Inspector(a) Arreglos",
        domain=['&', ('inspector', '=', True)]
    )

    # Funciones: 'Computadas'
    @api.model
    @api.depends('modelo_prenda_id')
    def get_data_from_modelo_prenda(self):
        if(self.modelo_prenda_id):
            env_modelo_prenda = self.env["modeloprenda.material.rel"]
            search_modelo_prenda = [("modelo_id",
                                     "=",
                                     self.modelo_prenda_id.id)]
            self.material_ids = env_modelo_prenda.search(search_modelo_prenda)
            self.codigo_modelo_sap = self.modelo_prenda_id.codigo_modelo_sap
            values = []
            env_tejido_partes = self.env['tejido.partes']
            search_tipo_prenda = [("tipo_prenda",
                                   "=",
                                   self.modelo_prenda_id.t_prenda)]
            env_tabla_operaciones = self.env['tejido.tablas.operaciones']
            for parte_tejido in env_tejido_partes.search(search_tipo_prenda):
                for operacion_tejido in parte_tejido.operaciones_ids:
                    st = ['&', ('header', '=', parte_tejido.tipo_parte),
                          '&', ('header_2', '=', parte_tejido.denominacion),
                          '&', ('option', '=', operacion_tejido.denominacion),
                          ('file_seguimiento_id', '=', self.id)]
                    combinacion = env_tabla_operaciones.search(st)
                    if(combinacion.id):
                        values += [(4, combinacion.id)]
                    else:
                        new_data = {'header': parte_tejido.tipo_parte,
                                    'header_2': parte_tejido.denominacion,
                                    'option': operacion_tejido.denominacion,
                                    'selected': False}
                        values += [(0, 0, new_data)]
            self.tabla_operaciones = values
            values = []
            for componente in self.modelo_prenda_id.componente_ids:
                denominacion = componente.componente_id.descripcion_componente
                new_data = {'componente_base_id': componente.id,
                            'denominacion': denominacion,
                            'cantidad': 1,
                            'cuadro_mallas_agujas': 0,
                            'cuadro_mallas_filas': 0,
                            'numero_cabos': componente.numero_cabos,
                            'dificultad': 'A',
                            'ancho_maximo': 0,
                            'punto_id': componente.punto_id,
                            'galga_id': componente.galga_id
                            }
                values += [(0, 0, new_data)]
            self.componentes_paneles_ids = values
        else:
            self.material_ids = []
            self.codigo_modelo_sap = ""
            self.tabla_operaciones = []
            self.componentes_paneles_ids = []

    @api.one
    @api.depends('tabla_tiempos')
    def actualizar_total_tiempo(self):
        total = 0
        for tiempo_u in self.tabla_tiempos:
            total += tiempo_u.tiempo_unitario
        self.tiempo_prenda = total

    # Funciones: 'On Change'
    @api.one
    @api.onchange('componentes_paneles_ids')
    def actualizar_datos_de_componente(self):
        if(len(self.componentes_paneles_ids) > 0):
            values = []
            for componente in self.componentes_paneles_ids:
                for cantidad in range(0, componente.cantidad):
                    component_name = componente.denominacion
                    if(componente.cantidad > 1):
                        component_name += (" (" + str(cantidad + 1) + ")")
                    values += [(0, 0, {'nombre_panel': component_name,
                                       'tiempo_bajada': 0,
                                       'cantidad': 1,
                                       'componente_id': componente})]
            self.tabla_tiempos = values
            values = []
            componentes = []
            max_guiahilos = 0
            for componente in self.componentes_paneles_ids:
                componentes += [[componente.denominacion,
                                 componente.maquina_id.numero_guia_hilos]]
                if(max_guiahilos < componente.maquina_id.numero_guia_hilos):
                    max_guiahilos = componente.maquina_id.numero_guia_hilos
            for componente in componentes:
                for i in range(0, max_guiahilos):
                    valor = ""
                    if(i >= componente[1]):
                        valor = "--"
                    values += [(0, 0, {'matrix_x': componente[0],
                                       'matrix_y': str(i+1),
                                       'value': valor})]
                values += [(0, 0, {'matrix_x': componente[0],
                                   'matrix_y': "Encoder",
                                   'value': ''})]
            self.tabla_guia_hilos = values
        else:
            self.tabla_tiempos = []
            self.tabla_guia_hilos = []

    @api.one
    @api.onchange('modelo_prenda_id', 'componentes_paneles_ids')
    def actualizar_pesos_y_porcentajes(self):
        if(self.modelo_prenda_id and (len(self.componentes_paneles_ids) > 0)):
            colores = ["Peso"]
            for color in self.modelo_prenda_id.color_ids:
                colores += [color.name_color]
            componentes = []
            for componente in self.componentes_paneles_ids:
                for cantidad in range(0, componente.cantidad):
                    component_name = componente.denominacion
                    if(componente.cantidad > 1):
                        component_name += (" (" + str(cantidad + 1) + ")")
                    componentes += [component_name]
            values = []
            env_tabla_pesos = self.env['tejido.tablas.pesos']
            for p in componentes:
                for e in colores:
                    search = ['&', ('matrix_x', '=', p),
                              '&', ('matrix_y', '=', e),
                              ('file_seguimiento_id', '=', self.id)]
                    combinacion_id = env_tabla_pesos.search(search).id
                    if(combinacion_id):
                        values += [(4, combinacion_id)]
                    else:
                        values += [(0, 0, {'matrix_x': p,
                                           'matrix_y': e,
                                           'value': ''})]
            self.tabla_pesos = values
        else:
            self.tabla_pesos = []

    # Funciones: 'Front-End'
    @api.one
    def actualizar_porcentajes(self):
        self.tabla_porcentajes = []
        values = []
        if(len(self.tabla_pesos) > 0):
            datos_registro = {}
            for registro in self.tabla_pesos:
                if registro.matrix_y in datos_registro:
                    datos_registro[registro.matrix_y] += registro.value
                else:
                    datos_registro[registro.matrix_y] = registro.value
            if(datos_registro["Peso"] != 0):
                for key in datos_registro:
                    datos_registro[key] *= 100
                    datos_registro[key] /= datos_registro["Peso"]
                    values += [(0, 0, {'matrix_x': '%',
                                       'matrix_y': key,
                                       'value': datos_registro[key]
                                       })]
            if(len(values) > 0):
                values.sort()
                values = [values.pop()] + values
                self.tabla_porcentajes = values

    @api.one
    def action_back(self):
        back_option = ''
        for i in file_status:
            if(i[0] == self.estado):
                break
            back_option = i[0]
        if(len(back_option)):
            self.write({'estado': back_option})

    @api.one
    def action_front(self):
        def get_medidas_values(file_id, relacion, componentes, medidas):
            env_relacion = self.env[relacion]
            values = []
            for componente in componentes:
                for medida in medidas:
                    search = ['&', ('matrix_x', '=', medida.codigo_medida),
                              '&', ('matrix_y', '=', componente.denominacion),
                              ('file_seguimiento_id', '=', file_id)]
                    registro = env_relacion.search(search)
                    if(registro.id):
                        values += [(4, registro.id)]
                    else:
                        values += [(0, 0, {'matrix_x': medida.codigo_medida,
                                           'matrix_y': componente.denominacion,
                                           'value': 0})]
            return values

        def get_pesos_obsv(file_id, relacion, componentes):
            env_relacion = self.env[relacion]
            values = []
            for componente in componentes:
                search = ['&', ('componente_panel_ids', '=', componente.id),
                          ('file_seguimiento_id', '=', file_id)]
                registro = env_relacion.search(search)
                if(registro.id):
                    values += [(4, registro.id)]
                else:
                    values += [(0, 0, {'componente_panel_ids': componente.id,
                                       'cantidad': componente.cantidad,
                                       'peso': 0,
                                       'observacion': ''})]
            return values
        front_option = ''
        exit_for = False
        for i in file_status:
            front_option = i[0]
            if(exit_for):
                break
            if(i[0] == self.estado):
                front_option = ''
                exit_for = True
        if(len(front_option)):
            if(front_option == "Lav"):
                v_ctec = get_medidas_values(self.id,
                                            'tejido.medidas.tecnico',
                                            self.componentes_paneles_ids,
                                            self.modelo_prenda_id.medida_ids)
                v_ct_po = get_pesos_obsv(self.id,
                                         'tej.tecn.comp',
                                         self.componentes_paneles_ids)
                self.write({'tabla_control_tecnico': v_ctec,
                            'control_tecnico_pesos_y_observaciones': v_ct_po})
            self.write({'estado': front_option})
