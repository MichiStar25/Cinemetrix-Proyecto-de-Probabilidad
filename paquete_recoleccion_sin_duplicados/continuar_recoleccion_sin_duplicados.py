import requests
import time
import os

API_KEY = "c960280ae74c7ca2cf38db74209ffcbc"
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

output_sql = "peliculas_40k_sin_duplicados.sql"
progreso_file = "progreso_final.txt"
ids_existentes_file = "ids_existentes.txt"

def get_movie_data(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=es-ES"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error con movie_id {movie_id}: {e}")
    return None

def clean_str(s):
    return s.replace("'", "''") if s else ""

def leer_ids_existentes():
    if os.path.exists(ids_existentes_file):
        with open(ids_existentes_file, "r", encoding="utf-8") as f:
            return set(map(int, f.read().strip().split(",")))
    return set()

def guardar_ids_existentes(ids):
    with open(ids_existentes_file, "w", encoding="utf-8") as f:
        f.write(",".join(map(str, ids)))

def leer_progreso():
    if os.path.exists(progreso_file):
        with open(progreso_file, "r") as f:
            lineas = f.read().strip().split(",")
            if len(lineas) == 2:
                return int(lineas[0]), int(lineas[1])
    return 1, 0

def guardar_progreso(movie_id, inserted):
    with open(progreso_file, "w") as f:
        f.write(f"{movie_id},{inserted}")

def main():
    movie_id, inserted = leer_progreso()
    ids_existentes = leer_ids_existentes()
    modo = "a" if inserted > 0 else "w"

    with open(output_sql, modo, encoding="utf-8") as f:
        if inserted == 0:
            f.write("""
CREATE DATABASE IF NOT EXISTS peliculas;
USE peliculas;

DROP TABLE IF EXISTS Peliculas;
CREATE TABLE IF NOT EXISTS Peliculas (
    id INT PRIMARY KEY,
    titulo VARCHAR(255),
    anio INT,
    mes INT,
    genero VARCHAR(100),
    clasificacion_edad VARCHAR(20),
    estudio VARCHAR(100),
    imdb_pelicula FLOAT
);
""")

        while inserted < 40000:
            if movie_id in ids_existentes:
                movie_id += 1
                continue

            movie = get_movie_data(movie_id)
            movie_id += 1

            if not movie or not movie.get("title"):
                continue

            ids_existentes.add(movie["id"])
            title = clean_str(movie.get("title", ""))
            release = movie.get("release_date", "0000-00-00")
            anio = int(release[:4]) if release[:4].isdigit() else 0
            mes = int(release[5:7]) if release[5:7].isdigit() else 0
            genero = clean_str(", ".join([g.get("name", "") for g in movie.get("genres", [])]))
            clasificacion = "18+" if movie.get("adult", False) else "PG"
            companias = movie.get("production_companies")
            if companias and isinstance(companias, list) and len(companias) > 0:
                estudio = clean_str(companias[0].get("name", ""))
            else:
                estudio = ""
            puntuacion = float(movie.get("vote_average", 0.0))

            sql = f"INSERT INTO Peliculas (id, titulo, anio, mes, genero, clasificacion_edad, estudio, imdb_pelicula) VALUES ({movie['id']}, '{title}', {anio}, {mes}, '{genero}', '{clasificacion}', '{estudio}', {puntuacion});\n"
            f.write(sql)
            inserted += 1

            if inserted % 100 == 0:
                print(f"Insertadas: {inserted}")
                guardar_progreso(movie_id, inserted)
                guardar_ids_existentes(ids_existentes)

            time.sleep(0.25)

        guardar_progreso(movie_id, inserted)
        guardar_ids_existentes(ids_existentes)
        print("Finalizado. 40,000 películas insertadas.")

if __name__ == "__main__":
    main()
