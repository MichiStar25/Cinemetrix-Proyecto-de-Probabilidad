import requests
import time
import os

API_KEY = "c960280ae74c7ca2cf38db74209ffcbc"
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

output_sql = "peliculas_40k_dump.sql"
progreso_file = "progreso.txt"

def get_movie_data(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=es-ES"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error con movie_id {movie_id}: {e}")
    return None

def get_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error obteniendo créditos para movie_id {movie_id}: {e}")
    return None

def clean_str(s):
    return s.replace("'", "''") if s else ""

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
    modo = "a" if inserted > 0 else "w"

    with open(output_sql, modo, encoding="utf-8") as f:
        if inserted == 0:
            f.write("""CREATE DATABASE IF NOT EXISTS peliculas;
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
    imdb_pelicula FLOAT,
    actor_principal VARCHAR(255),
    actor_rating FLOAT,
    actor_nominado BOOLEAN,
    actor_ganador BOOLEAN,
    director VARCHAR(255),
    director_rating FLOAT,
    director_nominado BOOLEAN,
    director_ganador BOOLEAN
);
""")

        while inserted < 40000:
            movie = get_movie_data(movie_id)
            credits = get_credits(movie_id)
            movie_id += 1

            if not movie or not movie.get("title"):
                continue

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

            actor = ""
            actor_rating = round(puntuacion - 0.5, 1)
            actor_nominado = "TRUE" if actor_rating > 6.0 else "FALSE"
            actor_ganador = "TRUE" if actor_rating > 7.5 else "FALSE"
            director = ""
            director_rating = round(puntuacion + 0.5, 1)
            director_nominado = "TRUE" if director_rating > 6.5 else "FALSE"
            director_ganador = "TRUE" if director_rating > 8.0 else "FALSE"

            if credits:
                cast = credits.get("cast", [])
                crew = credits.get("crew", [])
                if cast:
                    actor = clean_str(cast[0].get("name", ""))
                for person in crew:
                    if person.get("job") == "Director":
                        director = clean_str(person.get("name", ""))
                        break

            sql = f"INSERT INTO Peliculas (id, titulo, anio, mes, genero, clasificacion_edad, estudio, imdb_pelicula, actor_principal, actor_rating, actor_nominado, actor_ganador, director, director_rating, director_nominado, director_ganador) VALUES ({movie['id']}, '{title}', {anio}, {mes}, '{genero}', '{clasificacion}', '{estudio}', {puntuacion}, '{actor}', {actor_rating}, {actor_nominado}, {actor_ganador}, '{director}', {director_rating}, {director_nominado}, {director_ganador});\n"
            f.write(sql)
            inserted += 1

            if inserted % 100 == 0:
                print(f"Insertadas: {inserted}")
                guardar_progreso(movie_id, inserted)

            time.sleep(0.25)

    guardar_progreso(movie_id, inserted)
    print("Finalizado. 40,000 películas insertadas.")

if __name__ == "__main__":
    main()