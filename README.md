# Cinemetrix-Proyecto-de-Probabilidad
Documentos, Script, archivos

I. Descripción de los datos:

1. En el documento "Descripción de datos" se explica cada una de las variables, el tipo de dato y como queremos trabajar con ellas.

II. Análisis descriptivo

En la carpeta de "tmdb_sql_pack_desde_cero" se encuentran los siguientes elementos:
1. Un txt llamado "progreso" en el cual se define lo que se hizo para obtener la base de datos 
2. El script llamado "peliculas_tmdb" que se encargó de recolectar los datos de la página de TMDB, https://api.themoviedb.org/3; que con ayuda de una clave API que te da la página luego de unos requisitos, logra recopilar la información y guardarla en un archivo SQL
3. Y luego está la base de datos resultantes que posee duplicados.

En la carpeta "paquete_recolección_sin_duplicados":
1. Está el script Python que recolecta otra base de datos, pero esta vez no posee duplicados
2. Y esta el archivo sql resultante de la extracción del script

En la carpeta "base_de_datos_limpia_y_procesada" se encuentra lo siguiente
1. La base de datos final del grupo en un sql llamado "Cinemetrix"
2. Un script para pasar el sql a un archivo Excel "convertir_sql_a_excel"
3. Con las instrucciones de lo que hay que hacer para lograr pasar el sql a excel, en un txt "README"
4. El Excel resultante de ese script "peliculas_convertidas", el cual presentó errores en la conversión de varios datos, por lo que se optó por otra alternativa.
5. Aparece en txt "Instrucciones para pasar sql a csv" que explica lo que lleva como titulo
6. Y de ultimo está el CSV resultante de la expertación de la base de datos desde el mismo MySQL Workbench llamado "Base_de_datos_peliculas"

III. Análisis Estocásticos

Y a continuación están los análisis, gráficos y scripts del análisis estocástico de todo el proyecto:

https://colab.research.google.com/drive/1YUmL-9pPPwZL8Xg2OAwCn2o2slC48ErL?usp=sharing
1. En la carpeta de "Análisis Estocástico" se guardo la explicación de cada una de las graficas y los analisis finales de los resultados del modelo predictivo del problema planteado, es el archivo llamado "Explicación del Análisis"

IV. Documentos del Proyecto
En esta carpeta esta la propuesta, los avances y el reporte del proyecto, tambien posee el pdf del story telling
