# -*- coding: utf-8 -*-

import pyodbc
import sys
from collections import OrderedDict
from contextlib import contextmanager


@contextmanager
def connect_db_sap(commit=False):
    dsn = 'sqlserverdatasource'
    user = 'sa'
    password = 'SBOartatlas'
    database = 'sbo_atlas_produccion'

    con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user,
                                                        password, database)
    cnxn = pyodbc.connect(con_string)
    cursor = cnxn.cursor()

    # Know if autocommit is enabled
    # cnxn.autocommit

    try:
        yield cursor
    except pyodbc.DatabaseError as err:
        error, = err.args
        sys.stderr.write(error.message)
        cursor.rollback()
        raise err
    else:
        if commit:
            cursor.commit()
        else:
            cursor.rollback()
    finally:
        cursor.close()
        del cursor
        cnxn.close()


def get_avios():
    query_string = "SELECT T0.Itemcode as CodAvio, T0.ItemName as NomAvio, " \
                   "CASE WHEN T1.Code IS NULL THEN '' ELSE T1.Code END as " \
                   "CodColor, CASE WHEN T1.Name IS NULL THEN '' " \
                   "ELSE T1.Name END as NomColor, CASE WHEN T0.InvntryUom " \
                   "IS NULL THEN '' ELSE T0.InvntryUom END as UM from OITM " \
                   "T0 left join [dbo].[@SYP_AV_COLOR] T1 on " \
                   "T0.U_SYP_AVI_COLOR = T1.Code WHERE T0.[ItmsGrpCod]=102"
    dict_avio = {}
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        dict_avio = OrderedDict([(unicode(row.CodAvio),
                                  [unicode(row.NomAvio),
                                   unicode(row.NomColor),
                                   unicode(row.UM)])
                                 for row in rows])
    return dict_avio


def get_material():
    query_string = "SELECT distinct ItemCode as CodHilado, ItemName as " \
                   "NomHilado, U_SYP_HIL_CALIDA as Calidad, U_SYP_HIL_GROSOR" \
                   " as Titulo, U_SYP_HIL_COLOR as Color from OITM where " \
                   "ItmsGrpCod='100'"
    dict_material = {}
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()

        dict_material = OrderedDict([(row.CodHilado, row.NomHilado)
                                     for row in rows])

    return dict_material


def get_temporada():
    query_string = 'SELECT T0.[Code] FROM [dbo].[@AA_TEMPORADAS]  T0'
    lst_temporadas = []

    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        lst_temporadas = [(unicode(row.Code), unicode(row.Code))
                          for row in rows]

    return lst_temporadas


def get_grupo_talla():
    query_string = 'SELECT T0.[Code], T0.[Name]' \
                   'FROM [dbo].[@SYP_PT_GRUPOTALLA]  T0'
    dict_gtalla = {}

    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()

        dict_gtalla = OrderedDict([(unicode(row.Code), unicode(row.Name))
                                   for row in rows])

    return dict_gtalla


def get_tallasxgrupo(gtalla):
    query_string = "SELECT T0.[U_SYP_PT_TALLA] FROM [dbo].[@SYP_PT_TALLAS]" \
                   "T0 WHERE T0.[U_SYP_PT_CODGRUPOTAL] ='{0}'".format(gtalla)
    list_tallas = []

    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()

        list_tallas = [unicode(row[0]) for row in rows]

    return list_tallas


def get_clientes():
    query_string = "SELECT T0.[CardCode], CASE WHEN T0.CardFName IS NULL " \
                   "THEN T0.[CardName] ELSE T0.CardFName END AS Nombre FROM " \
                   "OCRD T0 WHERE T0.[CardType] ='c'"
    dic_cli = {}
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()

        dic_cli = OrderedDict([(unicode(row.CardCode), unicode(row[1]))
                               for row in rows])

    return dic_cli


def get_colorxtituloxcalidad(calidad, titulo):
    query_string = "SELECT COUNT(*) FROM OITM T0 WHERE " \
                   "T0.[U_SYP_HIL_CALIDA] ='{0}' and  " \
                   "T0.[U_SYP_HIL_GROSOR] ='{1}'".format(calidad, titulo)
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchone()
        result = rows[0]

    return result


def get_tprenda():
    query_string = "SELECT T0.[Code], T0.[Name]" \
                   "FROM [dbo].[@SYP_PT_TIPOPRENDA] T0 ORDER BY T0.[Code]"
    dict_tprenda = {}

    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()

        dict_tprenda = OrderedDict([(unicode(row.Code), unicode(row.Name))
                                    for row in rows])
    return dict_tprenda


def get_tproducto():
    query_string = "SELECT T0.[Code], T0.[Name] FROM [dbo].[@SYP_PT_TIPOPROD]"\
                   "T0 WHERE T0.[Code] <>'R' ORDER BY T0.[CODE] DESC"
    dict_tproducto = {}
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()

        dict_tproducto = OrderedDict([(unicode(row.Code), unicode(row.Name))
                                      for row in rows])

    return dict_tproducto


def get_genero():
    query_string = "SELECT T0.[Code], T0.[Name]" \
                   "FROM [dbo].[@SYP_PT_GENERO]  T0"
    dict_genero = {}
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()

        dict_genero = OrderedDict([(unicode(row.Code), unicode(row.Name))
                                   for row in rows])

    return dict_genero


def get_materialxcalidad(calidad):
    query_string = "SELECT T0.[U_SYP_DESCRIPCION] " \
                   "FROM [dbo].[@SYP_MP_CALIDADTELA]  T0 WHERE " \
                   "T0.[Code]='{0}'".format(calidad)
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        result = rows

    return '' if not result else result[0][0]


def get_presentacion():
    query_string = "SELECT * FROM [dbo].[@SYP_MP_PRESENTELA]"
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        result = rows

    return result


def get_procedencia():
    query_string = "SELECT * FROM [dbo].[@SYP_MP_PROCEDENCIA]"
    result = []

    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        result = rows

    return result


def get_cuenta_cliente(cliente):
    query_string = "SELECT left(T0.[DebPayAcct],2) "\
                   "FROM OCRD T0 WHERE T0.[CardCode] = '{0}'".format(cliente)
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchone()
        result = rows[0]

    return result


def get_exist_model(codigo_modelo_sap):
    query_string = "select count(*) from TIPODECAMBIO.dbo.[@SYP_PT_MODELO] " \
                   "where U_SYP_AA_COMOD = '{0}'".format(codigo_modelo_sap)
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchone()
        result = rows[0]

    return True if result > 0 else False


def set_modelo_sap_sp(**data):
    query_string = "exec [ITSM_INSERT_MODELO] '%s', '%s', '%s', '%s', " \
                   "'%s', '%s'" % (data['U_SYP_AA_COMOD'],
                                   data['U_SYP_AA_DESCMOD'],
                                   data['U_SYP_CL_COMOD'],
                                   data['U_SYP_CL_DESCMOD'],
                                   data['U_SYP_DESCCOMP'],
                                   data['U_SYP_CODANT'])

    with connect_db_sap(commit=True) as cursor:
        cursor.execute(query_string.encode('utf-8'))

    return


def update_modelo_sap_sp(**data):
    query_string = "exec [ITSM_UPDATE_MODELO] '%s', '%s', '%s', " \
                   "'%s', '%s'" % (data['U_SYP_AA_COMOD'],
                                   data['U_SYP_AA_DESCMOD'],
                                   data['U_SYP_CL_COMOD'],
                                   data['U_SYP_CL_DESCMOD'],
                                   data['U_SYP_DESCCOMP'])
    with connect_db_sap(commit=True) as cursor:
        cursor.execute(query_string.encode('utf-8'))
    return


def get_len_calidad_hilado():
    query_string = "SELECT COUNT(distinct T0.[U_SYP_HIL_CALIDA]) FROM OITM " \
                   "T0 WHERE T0.[U_SYP_HIL_CALIDA] is not null"
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchone()
        result = rows[0]

    return result


def get_calidad_hilado():
    query_string = "SELECT distinct T0.[U_SYP_HIL_CALIDA] FROM OITM T0 WHERE" \
                   " T0.[U_SYP_HIL_CALIDA] is not null"
    lst_calidades = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        lst_calidades = [unicode(row[0]) for row in rows]

    return lst_calidades


def get_len_calidad_tela():
    query_string = "SELECT COUNT(*) FROM [dbo].[@MTH_CODTELA]"
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchone()
        result = rows[0]

    return result


def get_calidad_tela():
    query_string = "SELECT T0.[Code], T0.[Name] FROM [dbo].[@MTH_CODTELA]  T0"
    lst_calidades = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        lst_calidades = [unicode(row[1]) for row in rows]

    return lst_calidades


def get_len_titulos_hilado():
    query_string = "SELECT COUNT(distinct T0.[U_SYP_HIL_GROSOR]) FROM OITM "\
                   "T0 where T0.[U_SYP_HIL_GROSOR] is not null"
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchone()
        result = rows[0]

    return result


def get_titulos_tela():
    query_string = "SELECT T0.[Name] FROM " \
                   "[dbo].[@SYP_MP_TITULOHILADO] T0"
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        result = [unicode(row[0]) for row in rows]

    return result


def get_len_titulos_tela():
    query_string = "SELECT COUNT(T0.[Name]) FROM " \
                   "[dbo].[@SYP_MP_TITULOHILADO] T0"
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchone()
        result = rows[0]

    return result


def get_len_titulos_calidad():
    query_string = "SELECT T0.[U_SYP_HIL_CALIDA], COUNT(DISTINCT " \
                   "T0.[U_SYP_HIL_GROSOR]) FROM OITM T0 WHERE " \
                   "T0.[U_SYP_HIL_CALIDA] IS NOT NULL GROUP BY " \
                   "T0.[U_SYP_HIL_CALIDA]"
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        result = [(unicode(row[0]), row[1]) for row in rows]

    return result


def get_titulosxcalidad(calidad):
    query_string = "SELECT distinct T0.[U_SYP_HIL_GROSOR] FROM OITM T0 " \
                   "WHERE T0.[U_SYP_HIL_CALIDA] ='{0}'".format(calidad)
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()

        result = [unicode(row[0]) for row in rows]

    return result


def get_materiales():
    query_string = "SELECT T0.[Code], T0.[U_SYP_DESCRIPCION] "\
                   "FROM [dbo].[@SYP_MP_CALIDADTELA] T0"
    result = []
    with connect_db_sap() as cursor:
        cursor.execute(query_string)
        rows = cursor.fetchall()
        result = rows

    return result


def main():
    pass


if __name__ == '__main__':
    main()
