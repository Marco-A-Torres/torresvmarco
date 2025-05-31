import sqlite3

# Ruta de la base de datos
db_path = 'playlist_expert_system.db'

try:
    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Listar todas las tablas en la base de datos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if tables:
        print("Tablas disponibles en la base de datos:")
        for table in tables:
            print(f" - {table[0]}")
        
        # Verificar si 'songs' está entre las tablas
        if any(table[0] == 'songs' for table in tables):
            print("\nLa tabla 'songs' existe en la base de datos.")
            
            # Mostrar las columnas de la tabla 'songs'
            cursor.execute("PRAGMA table_info(songs);")
            columns = cursor.fetchall()
            print("Columnas de la tabla 'songs':")
            for col in columns:
                print(f" - {col[1]} (Tipo: {col[2]})")
            
            # Mostrar algunas filas de 'songs' para confirmar datos
            cursor.execute("SELECT * FROM songs LIMIT 5;")
            rows = cursor.fetchall()
            if rows:
                print("\nAlgunas filas en 'songs':")
                for row in rows:
                    print(row)
            else:
                print("\nLa tabla 'songs' está vacía.")
        else:
            print("La tabla 'songs' no existe en la base de datos.")
    else:
        print("No se encontraron tablas en la base de datos.")
        
except sqlite3.Error as e:
    print("Error al conectar con la base de datos:", e)
finally:
    # Cerrar la conexión
    conn.close()
