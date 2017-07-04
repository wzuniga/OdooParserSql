# -*- coding: utf-8 -*-

import urllib2
from xml.etree import cElementTree as ET, ElementTree as ETX
from xml import etree as xmltree
from openerp.exceptions import ValidationError


def get_group_code_client(t_producto, cuenta_cliente, codigo_garticulo):
    if (t_producto == 'M'):
        if(cuenta_cliente == '12'):
            code = '116'
        else:
            code = '117'
    else:
        if (codigo_garticulo == 'TP'):
            if(cuenta_cliente == '12'):
                code = '110'
            else:
                code = '111'
        elif (codigo_garticulo == 'CP'):
            if(cuenta_cliente == '12'):
                code = '114'
            else:
                code = '115'
        else:
            raise ValidationError('Sólo se puede realizar la migración a SAP '
                                  ' para los Grupos de Artículos TEJIDO PUNTO '
                                  ' y CONFECCIÓN PRENDAS')

    return code


def migrate_sap_database(**data):

    _user = 'B1iadmin'
    _pass = 'SBOartatlas44'
    _host = "http://192.168.0.7:8080/"

    _url = 'B1iXcellerator/exec/soap/' \
           'vP.0010000106.in_WCSX/com.sap.b1i.vplatform.runtime/' \
           'INB_WS_CALL_SYNC_XPT/INB_WS_CALL_SYNC_XPT.ipo/proc'

    _envelope = "http://schemas.xmlsoap.org/soap/envelope/"

    headers = {'content-type': 'text/xml'}

    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, _host, _user, _pass)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

    _group_code_client = get_group_code_client(data['_tproducto'],
                                               data['_cuenta_cliente'],
                                               data['_codigo_garticulo'])
    _code_model_sap = data['_codigo_modelo_sap']

    if(len(data['_colors_list']) > 1):
        colors_list = ["C{:0>3}".format(i) for i in range(1, data['_nro_cmb'])]
    else:
        colors_list = [c.value_color for c in data['_colors_list']]

    codlist = []
    for talla in data['tallas_list']:
        for color in colors_list:
            codigo = '{0}{1}{2}{3}{4}'.format(data['_codigo_modelo_sap'],
                                              data['_gtallas'],
                                              'G',
                                              color,
                                              talla)

            Envelope = ET.Element("soapenv:Envelope")
            Envelope.attrib["xmlns:soapenv"] = _envelope
            ET.SubElement(Envelope, "soapenv:Header")
            Body = ET.SubElement(Envelope, "soapenv:Body")
            ProductoTerminado = ET.SubElement(Body, "ProductoTerminado")
            row = ET.SubElement(ProductoTerminado, "row")
            ET.SubElement(row, "ItemCode").text = codigo
            ET.SubElement(row, "ItemName").text = data['_denominacion_modelo']
            ET.SubElement(row, "ItemType").text = "I"
            ET.SubElement(row, "ItemsGroupCode").text = _group_code_client
            ET.SubElement(row, "GLMethod").text = "C"
            ET.SubElement(row, "CostAccountingMethod").text = "A"
            ET.SubElement(row, "ManageStockByWarehouse").text = "Y"
            ET.SubElement(row, "VatLiable").text = "Y"
            ET.SubElement(row, "WTLiable").text = "Y"
            ET.SubElement(row, "IndirectTax").text = "Y"
            ET.SubElement(row, "ApTaxCode").text = "IGV"
            ET.SubElement(row, "ArTaxCode").text = "IGV"
            ET.SubElement(row, "PurchaseItem").text = "N"
            ET.SubElement(row, "SalesItem").text = "Y"
            ET.SubElement(row, "InventoryItem").text = "Y"
            ET.SubElement(row, "ManageBatchNumbers").text = "N"
            ET.SubElement(row, "InventoryUOM").text = "UND"
            ET.SubElement(row, "DefaultWarehouse").text = "07"
            ET.SubElement(row, "U_SYP_PT_TIPOPRE").text = data['_tprenda']
            ET.SubElement(row, "U_SYP_PT_GENERO").text = data['_genero']
            ET.SubElement(row, "U_SYP_PT_FAMIL").text = data['_familia']
            ET.SubElement(row, "U_SYP_PT_TIPOPRO").text = data['_tproducto']
            ET.SubElement(row, "U_SYP_PT_DISEN").text = data['_disen']
            ET.SubElement(row, "U_SYP_PT_GRUTALL").text = data['_gtallas']
            ET.SubElement(row, "U_SYP_PT_GRUCOL").text = 'G'
            ET.SubElement(row, "U_SYP_PT_TALLA").text = talla
            ET.SubElement(row, "U_SYP_PT_COLOR").text = color
            ET.SubElement(row, "U_SYP_PT_MODELO").text = _code_model_sap

            SM_TEMPLATE = xmltree.ElementTree.tostring(
                Envelope,
                encoding='utf-8',
                method='xml')
            SoapMessage = SM_TEMPLATE

            request = urllib2.Request(_host + _url, SoapMessage, headers)
            response = urllib2.urlopen(request)
            result = response.read()
            root = ETX.fromstring(result)

            _error_msg = 'Error: Ya existe el Producto Terminado'
            _success_msg = 'Se creó el código SAP correctamente'

            if(response.getcode() == 200):
                if (root[0][0][0].text == _error_msg):
                    codlist.append("{0} = {1}".format(codigo, _error_msg))
                else:
                    codlist.append("{0} = {1}".format(codigo, _success_msg))

    return codlist
