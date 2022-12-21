import psycopg2

# Connect to an existing database
with psycopg2.connect(user="iflores_c",
        password="Flores.36",
        host="10.7.83.17",
        port="5432",
        database="fs_venta_cartera_nov"
        ) as conn:
    
    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        
        # Execute a command: Select rows of table
        # Query the database and obtain fata python objects

        query   = """SELECT idsucaux,idproducto,idauxiliar,kauxiliar,vin, FROM deudores INNER JOIN ofx_multicampos_sustentable.auxiliar_masdatos USING(kauxiliar) LIMIT 10"""
        query_1 = """SELECT COUNT(*) FROM deudores"""

        cur.execute(query_1)

        cur.fetchone()

        for record in cur:
            print(list(record))

        # Make the changes to the database persistent
        conn.commit

        
