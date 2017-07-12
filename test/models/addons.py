class Punto(models.Model):
    _inherit = 'desarrollo.punto'


class Galga(models.Model):
    _inherit = 'desarrollo.galga'


class ModeloPrendaComponenteRel(models.Model):
    _inherit = 'modeloprenda.componente.rel'


class ModeloPrenda(models.Model):
    _inherit = 'desarrollo.modelo.prenda'
