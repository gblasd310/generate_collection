import pandas as pd
from MyDataBase import MyDataBase

openfin_s = 'user=iflores_c password=Flores.36 host=172.17.100.14 port=5432 dbname=openfin_s'
db =  MyDataBase(openfin_s)

# Read the file xlsx as DataFrame
df = pd.read_excel("C:/openfin_data/data/Files/RecaudosDetalladosPorEstacion (20).xlsx")

# Delete the first row
df.drop([0], axis=0, inplace=True)

# Set name of columns
df.columns = list(df.iloc[0])
#print(list(df.iloc[0]))

# Delete the first row with the name of columns
df.drop([1], axis=0, inplace=True)

#print(df)

# Delete column NaN
df = df[df.columns[-13:]]
#print(df)

# Add column
df["Sobreprecio"] = ""
df["Credito"] = ""
df["Cliente"] = ""
df["2001"] = ""

#print(df)

for i in range(2, len(df)):
    # Calculate and add the OVERPRICE
    df.loc[i,'Sobreprecio'] = float(df.iloc[i]['Abono']) / float(df.iloc[i]['Cantidad'])

    # Get data of database with the 
    placa = df.loc[i,"Placa "]

    # Delete spaces to string
    placa = str(placa).strip()

    # print(placa, end = ' >>> ')
    if placa.startswith('0'):
        placa = str(placa)[1:]

    # QUERY Placa with 0 
    query_exec = "SELECT idsucaux ||'-'|| idproducto ||'-'|| idauxiliar FROM deudores WHERE  referencia = '{0}';".format(placa)
    # Execute query
    result = db.query(query_exec)
    # Set value to row
    row = db.cur.fetchone()
    if not row:
        # print('Not row')
        df.loc[i, 'Credito'] = ''
    else:
        # print(list(row))
        df.loc[i, 'Credito'] = list(row)[0]

        row = list(row)
        credit = str(row[0]).split('-')
        idsucaux, idproducto, idauxiliar = credit[0], credit[1], credit[2]
        print(idsucaux, '-' ,idproducto,'-' , idauxiliar)

        # QUERY Placa with 0 
        query_exec = "SELECT idsucursal ||'-'|| idrol ||'-'|| idasociado FROM deudores WHERE  referencia = '{0}';".format(placa)
        # Execute query
        result = db.query(query_exec)
        # Set value to row
        row = db.cur.fetchone()
        df.loc[i, 'Cliente'] = list(row)[0]

        # QUERY Placa with 0 
        query_exec = "SELECT idsucauxref ||'-'|| idproductoref ||'-'|| idauxiliarref FROM auxiliares_ref WHERE (idsucaux, idproducto, idauxiliar) = ({},{},{});".format(idsucaux, idproducto, idauxiliar)
        # Execute query
        result = db.query(query_exec)
        # Set value to row
        row = db.cur.fetchone()
        df.loc[i, '2001'] = list(row)[0]


    if i == 100:
        break


# for i in range(2, 20):
#    print(df.loc[i])
print(df)
