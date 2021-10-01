import pandas as pd
import numpy as np
import sqlite3

#creamos la función para calcular el grupo de edad al que pertenecen los clientes
def age_group(x):
    if x <= 20:
        return 1
    if x > 20 and x<=30:
        return 2
    if x > 30 and x<=40:
        return 3
    if x > 40 and x<=50:
        return 4
    if x > 50 and x<=60:
          return 5
    if x > 60:
        return 6
    return 0


#Se leen los datos del acrhivo clientes.csv y se eliminan las filas con datos faltantes
df=pd.read_csv("clientes.csv",sep=';',na_filter=True)
df.dropna(inplace=True)
#limpiamos y transformamos nuestros datos
df["prioridad"]=df["prioridad"].astype(int)
df[["fiscal_id","first_name","last_name","gender","direccion","correo", "estatus_contacto"]]=df[["fiscal_id","first_name","last_name","gender","direccion","correo", "estatus_contacto"]].apply(lambda x: x.str.upper())
df["telefono"]=df['telefono'].astype(str).str.rsplit(".",expand=True)[0]
#generamos nuestro nuevo archivo clientes y  renombramos las columnas
clientes=df[["fiscal_id","first_name","last_name","gender","fecha_nacimiento","fecha_vencimiento","deuda","direccion"]]
clientes=clientes.rename(columns={ 'fecha_nacimiento':'birth_date','fecha_vencimiento':'due_date','deuda':'due_balance','direccion':'address'})
#transformamos las fechas de string a datetime
clientes['birth_date']=pd.to_datetime(clientes['birth_date'])
clientes['due_date']=pd.to_datetime(clientes['due_date'])
#calculamos el atributo 'age','deliquency' y 'age group'
clientes['age'] =pd.to_datetime("today").year-clientes['birth_date'].apply(lambda x: x.year)
clientes['delinquency'] =pd.to_datetime("today")-clientes['due_date']
clientes['delinquency']=clientes['delinquency'].dt.days
clientes["age_group"]=clientes["age"].apply(lambda x: age_group(x))
#colamos en orden los atributos
clientes = clientes.reindex(columns=['fiscal_id',
                                      'first_name',
                                      'last_name',
                                      'gender',
                                      'birth_date',
                                      'age',
                                      'age_group',
                                      'due_date',
                                      'delinquency',
                                      'due_balance',
                                      'address'
                                   ])
#transformamos a tipo de variable date
clientes['birth_date']=clientes['birth_date'].dt.date
clientes['due_date']=clientes['due_date'].dt.date
#colocamos 'fiscal_id' de index
clientes.set_index("fiscal_id",inplace=True)

#generamos nuestro nuevo archivo 'emails' y  renombramos las columnas
emails=df[["fiscal_id",'correo','estatus_contacto','prioridad']]
emails=emails.rename(columns={'correo':'email','estatus_contacto':'status','prioridad':'priority'})
emails.set_index("fiscal_id",inplace=True)
#generamos nuestro nuevo archivo 'phone' y  renombramos las columnas
phone=df[["fiscal_id",'telefono','estatus_contacto','prioridad']]
phone=phone.rename(columns={'telefono':'phone','estatus_contacto':'status','prioridad':'priority'})
phone.set_index("fiscal_id",inplace=True)
#guardamos los archivos en formato '.xlsx' en el directorio 'output'
clientes.to_excel (r'output/clientes.xlsx', header=True)
emails.to_excel (r'output/emails.xlsx', header=True)
phone.to_excel (r'output/phone.xlsx', header=True)
#guardamos los archivos  en la base de dato 'database'

bd = sqlite3.connect('database.db3')
clientes.to_sql(name='clientes', con=bd)
emails.to_sql(name='emails', con=bd)#
phone.to_sql(name='phone', con=bd)
bd.close()                         
