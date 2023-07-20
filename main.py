import pymysql.cursors
import os


class DB():

    """
         #cur.execute(vsql)
        #result = cur.fetchall()
    """


    def __init__(self):
        dbServer = 'localhost'
        dbUser = 'root'
        dbPass = 'dalas.2009'
        dbBase = 'comunadb'

        result = ""

        db = pymysql.connect(host=dbServer, user=dbUser, passwd=dbPass, db=dbBase)

        self.cur = db.cursor()


    def select(self, sql):

        self.cur.execute(sql)
        r = self.cur.fetchall()
        if r:
            return r[0][0]

    def insert(self, sql):

        self.cur.execute(sql)


db = DB()

def ultimo_recibo():

    q = """ 
            SELECT numero FROM comunadb.numeros where tipo = 'RECIBO';
    """

    r = db.select(q)

    return r


def csv2sql(archivo):

    nro_recibo = int(ultimo_recibo())
    sql = ""

    with open(archivo,"r") as f:
        for ff in f:
            l = ff.split(",")
            mes = l[0]
            vence = l[1]
            total = l[11].strip()
            ano = l[2]

            mes2 = men2num(mes)

            ## making
            mes2 = men2num(mes)

            periodo_anomes = f"{str(mes2).zfill(2)}/{ano}"
            id_contribuyentes = 1638
            nro_recibo += 1

            if len(vence)  == 9:
                fecha_vencimiento = f"{vence[5:9]}-{vence[2:4]}-{vence[0:1]}"
            else:
                fecha_vencimiento = f"{vence[6:9]}-{vence[3:5]}-{vence[0:2]}"

            fecha_emision = "2023-07-01"
            importe_total = total


            ## making sql

            campos = "nro_recibo,periodo_anomes,id_contribuyentes,fecha_emision,fecha_vencimiento,importe_total,fecha_vencimiento2,importe_total2,fecha_vencimiento3,importe_total3,id_tipos_zonas, id_estados"
            valores = f"{nro_recibo},'{periodo_anomes}',{id_contribuyentes},'{fecha_emision}','{fecha_vencimiento}',{importe_total},'{fecha_vencimiento}',{importe_total},'{fecha_vencimiento}',{importe_total},{1},'{'IM'}'"
            sql += f"insert into recibo_resumen ({campos}) values ({valores});"

        sql2 = f"UPDATE numeros SET numero = '{nro_recibo}' WHERE id_numeros = '1';"


        sql = sql + sql2

        print(sql)


def men2num(mes):
    j = "enero,febrero,marzo,abril,mayo,junio,julio,agosto,septiembre,octubre,noviembre,diciembre"
    aj = j.split(",")
    n  =  aj.index(mes.lower().strip())
    return n+1



csv2sql("ferrocarril.csv")









