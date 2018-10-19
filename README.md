Copiar previamente las imágenes de Manga109 en la carpeta /data/

```
python preprocessing.py
```

cuando se acabe el proceso, las imágenes preprocesadas estarán en la carpeta /manga/ , entonces

```
python main.py
```

para que se entrene la red neuronal y para evaluar los resultados

```
python test.py
````

correr la aplicación en máquina local

```
FLASK_APP=server.py flask run
```

y luego habilitar el túnel con ngrok


```
ngrok http 5000
```
