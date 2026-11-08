# Laboratorio: Código Seguro y Modelo OWASP

## 1. Datos generales

- **Nombre completo:** Carlos Mario Ayala Amaya
- **Carné:** TSU-C001
- **Correo institucional:** carlosmarioayala.1@gmail.com
- **Asignatura:** Lenguajes de Programación con Aspectos de Seguridad
- **Unidad:** Unidad 3 — Código Seguro y Modelo OWASP
- **Tutora:** Dámaris Alas
- **Periodo:** 02 al 08 de noviembre
- **Fecha:** 8 noviembre de 2026
- **Repositorio:** https://github.com/carlosmarioay/lab-las

## 2. Descripción

Este laboratorio consiste en desarrollar una aplicación web utilizando Python, implementando controles básicos de seguridad basados en buenas prácticas y el modelo OWASP. Se aplican mecanismos de validación de entradas, consultas parametrizadas, protección de contraseñas, registro de eventos de autenticación y detección de incidentes, incluyendo el cálculo de las métricas MTTD y MTTR.

## 3. Estructura del proyecto

```text
lab-las/
├── app.py             # Aplicación Flask (registro/login, validaciones, hash, eventos)
├── crearDB.py         # Crea usuarios.db con tabla usuarios(id, usuario, correo, password)
├── detector.py        # Detecta >=3 LOGIN_FALLIDO, bloquea (simulado) y calcula MTTD/MTTR
├── requirements.txt   # Dependencias (flask)
├── templates/
│   ├── registro.html  # Formulario de registro
│   └── login.html     # Formulario de login
├── usuarios.db        # Base de datos SQLite (generada con crearDB.py)
├── eventos.log        # Registro de LOGIN_CORRECTO / LOGIN_FALLIDO (generado en uso)
└── respuesta.log      # Registro de USUARIO_BLOQUEADO (generado por detector.py)
```

## 4. Ejecución del proyecto

**Paso 1.** Clonar el repositorio.

```bash
git clone https://github.com/carlosmarioay/lab-las
```

**Paso 2.** Ingresar al proyecto.

```bash
cd lab-las
```

**Paso 3.** Instalar las dependencias.

```bash
pip install -r requirements.txt
```

**Paso 4.** Crear la base de datos.

```bash
python crearDB.py
```

**Paso 5.** Ejecutar la aplicación.

```bash
python app.py
```

- Inicio: http://127.0.0.1:5000
- Registro: http://127.0.0.1:5000/registro
- Login: http://127.0.0.1:5000/login

**Paso 6.** Ejecutar el detector (en otra terminal).

```bash
python detector.py
```

## 5. Seguridad implementada

- Validación: usuario `[A-Za-z0-9_]{4,20}`, correo con regex, contraseña ≥ 8 caracteres.
- Normalización con `strip()` + `.get()` (sin quitar espacios internos de la contraseña).
- Hash con `generate_password_hash` / `check_password_hash` (scrypt, no texto plano).
- Consultas parametrizadas con `?` (resistente a inyección SQL).
- Detección de duplicados (`usuario` o `correo` ya registrado).
- Registro de eventos en `eventos.log` y respuesta simulada en `respuesta.log`.

## 6. Pruebas MTTD / MTTR

Procedimiento (Parte 4 Paso 6): por cada prueba se realizaron 3 intentos fallidos dejando segundos entre cada uno, luego `python detector.py`.

| Prueba | MTTD | MTTR |
|---|---|---|
| 1 (espera 2s) | 5.0 s | 1.0 s |
| 2 (espera 3s) | 7.0 s | 0.0 s |
| 3 (espera 5s) | 11.0 s | 0.0 s |

```
MTTD promedio = (5.0 + 7.0 + 11.0) / 3 = 7.67 s
MTTR promedio = (1.0 + 0.0 + 0.0) / 3 = 0.33 s
```

- **MTTD** = Detección (3er intento fallido) − Primer intento.
- **MTTR** = Respuesta (bloqueo simulado en `respuesta.log`) − Detección.
