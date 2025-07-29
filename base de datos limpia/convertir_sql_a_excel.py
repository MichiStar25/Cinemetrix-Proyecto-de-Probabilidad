import re
import pandas as pd

# 📍 Ruta del archivo SQL
ruta_sql = r'C:\Users\rashe\OneDrive - Universidad Tecnológica de Panamá\Visual Studio\base de datos limpia\peliculas_40k_limpias.sql'

# 🔧 Columnas esperadas
columnas = [
    'id', 'titulo', 'anio', 'mes', 'genero_raw', 'clasificacion_edad', 'estudio',
    'imdb_pelicula', 'actor_principal', 'actor_rating', 'actor_nominado', 'actor_ganador',
    'director', 'director_rating', 'director_nominado', 'director_ganador'
]

# 🧹 Limpiar el campo de género
def limpiar_generos(texto):
    if texto is None:
        texto = ''
    texto = texto.replace("'", '"')
    generos = re.findall(r'"([^"]+)"', texto)
    generos_limpios = sorted(set(g.strip() for g in generos if g.strip()))
    return ", ".join(generos_limpios)

# 📥 Procesar el archivo
datos = []

with open(ruta_sql, 'r', encoding='utf-8') as archivo:
    for linea in archivo:
        if 'INSERT INTO' not in linea:
            continue

        grupos = re.findall(r'\((.*?)\)', linea)
        for grupo in grupos:
            partes = re.split(r',(?=(?:[^\'"]|\'[^\']*\'|"[^"]*")*$)', grupo)
            partes = [p.strip().strip('"').strip("'") for p in partes]

            # ⛔ Evitar filas que accidentalmente contengan nombres de columnas
            if partes[0].lower() == 'id':
                continue

            fila = {}
            for i in range(len(columnas)):
                fila[columnas[i]] = partes[i] if i < len(partes) else None

            fila['resto'] = ', '.join(partes[len(columnas):]) if len(partes) > len(columnas) else ''
            fila['genero'] = limpiar_generos(fila.get('genero_raw'))

            datos.append(fila)

# 📦 Exportar a Excel
df = pd.DataFrame(datos)
df.to_excel('peliculas_convertidas.xlsx', index=False)
print('✅ Archivo generado sin duplicar encabezados: peliculas_convertidas.xlsx')
