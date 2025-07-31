# Cinemetrix-Proyecto-de-Probabilidad
Documentos, Script, archivos

Descripción de los datos:

1. En el documento "Descripción de datos" se explica cada una de las valiables, el tipo de dato y como queremos trabajar con ellas

Análisis descriptivo

En la carpera de "tmdb_sql_pack_desde_cero" se encuentra lo siguiente:
1. Un txt llamado "progreso" en el cual se define lo que se hizo para obtener la base de datos 
2. El script llamado "peliculas_tmdb" que se encargó de recolectar los datos de la página de la página de TMDB, https://api.themoviedb.org/3; que con ayuda de una clave API que te da la página luego de unos requisitos, logra recopilar los datos en un archivo sql
3. Y luego está la base de datos resultantes que posee duplicados.

En la carpeta "paquete_recolección_sin_duplicados":
1. Esta el script Python que recolecta otra base de datos, pero esta vez no posee duplicados
2. Y esta el archivo sql resultante de la extracción del script

En la carpeta "base_de_datos_limpia_y_procesada" aparece lo siguiente
1. La base de datos final del grupo en un sql llamado "Cinemetrix"
2. Un script para pasar el sql a un archivo Excel "convertir_sql_a_excel"
3. Con las instrucciones de lo que hay que hacer para lograr pasar el sql a excel, en un txt "README"
4. El Excel resultante de ese script "peliculas_convertidas", las cuales al visualizar nos damos de cuenta de que muchos de los datos no se pasaron correctamente, así que tuvimos que buscar otra opción 
5. Aparece en txt "Instrucciones para pasar sql a csv" que explica lo que lleva como titulo
6. Y de ultimo está el CSV resultante de la expertación de la base de datos desde el mismo MySQL Workbench llamado "Base_de_datos_peliculas"

Análisis Estocásticos

Y a continuación están los análisis, gráficos y scripts del análisis estocástico de todo el proyecto:

https://colab.research.google.com/drive/1YUmL-9pPPwZL8Xg2OAwCn2o2slC48ErL?usp=sharing
1. En la carpeta de "Análisis Estocástico" se guardo la explicación de cada una de las graficas y los analisis finales de los resultados del modelo predictivo del problema planteado, es el archivo llamado "Explicación del Análisis"
