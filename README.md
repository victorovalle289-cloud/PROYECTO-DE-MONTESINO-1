# Proyecto de Montesino - Gestor de contraseñas (CRUD Python-Flask)

## Estructura
```
proyecto de montesino/
├── BaseDeDatos/gestor_contrasena.sql
├── Backend/  (app.py, .flaskenv, requeriments.txt, .gitignore)
├── Frontend/ (index.html, add.html, edit.html, estilos.css, app.js, imagenes/)
└── Postman_coleccion.json
```

## Paso 1: Base de datos
Abre MySQL Workbench (o XAMPP/phpMyAdmin) y ejecuta `BaseDeDatos/gestor_contrasena.sql`.
Si tu usuario/clave de MySQL no es `root` / `1234`, cámbialo arriba en `Backend/app.py` (DB_USER, DB_PASS).

## Paso 2: Backend (en la terminal de VS Code)
```
cd Backend
python -m venv venv
venv\Scripts\activate          (Windows)   |   source venv/bin/activate (Mac/Linux)
pip install -r requeriments.txt
flask run
```
Queda corriendo en http://127.0.0.1:5000 — documentación Swagger en http://127.0.0.1:5000/apidocs

## Paso 3: Frontend
Abre `Frontend/index.html` con la extensión Live Server de VS Code (clic derecho > Open with Live Server).

## Paso 4: Pruebas con Postman
Postman > Import > selecciona `Postman_coleccion.json`. Ejecuta en orden:
dos registros (POST), dos consultas (GET), dos actualizaciones (PUT) y dos borrados (DELETE).

| Acción | Método | URL | Body (JSON) |
|---|---|---|---|
| Consulta general | GET | /  | - |
| Consulta individual | GET | /consulta_individual/1 | - |
| Registro | POST | /registro/ | {"plataforma":"Facebook","usuario":"victor","clave":"123abc"} |
| Actualizar | PUT | /actualizar/1 | {"plataforma":"Facebook","usuario":"victor_ff","clave":"nueva123"} |
| Eliminar | DELETE | /eliminar/1 | - |

## Paso 5: GitHub
```
git init
git add .
git commit -m "Proyecto de Montesino - CRUD Flask"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/proyecto-de-montesino.git
git push -u origin main
```
