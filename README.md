# Laboratorio LAS — MTTD y MTTR

Aplicación web en Python (Flask + SQLite) con validación de entradas,
hash de contraseñas, consultas parametrizadas, registro de eventos de
autenticación y detector de incidentes que calcula MTTD y MTTR.

## Estructura

```
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

## Cómo ejecutar

```bash
cd lab-las
pip install -r requirements.txt
python crearDB.py
python app.py
```

- Inicio: http://127.0.0.1:5000
- Registro: http://127.0.0.1:5000/registro
- Login: http://127.0.0.1:5000/login

## Cómo probar MTTD / MTTR

1. Registra un usuario válido (ej. `usuario_01` / `usuario@correo.com` / 8+ caracteres).
2. Haz 1 login correcto, luego 3 logins con contraseña incorrecta (deja segundos entre cada uno), luego 1 login correcto.
3. En otra terminal ejecuta:

```bash
python detector.py
```

Salida esperada:

```
ALERTA DE SEGURIDAD
Usuario: usuario_01
Intentos fallidos: 3
Primer intento: 2026-09-17 15:11:05
Detección: 2026-09-17 15:11:18
Acción aplicada: bloqueo de usuario
Respuesta: 2026-09-18 08:40:32
MTTR: ... segundos
MTTD: ... segundos
```

- **MTTD** = Detección (3er intento fallido) − Primer intento.
- **MTTR** = Respuesta (bloqueo simulado en `respuesta.log`) − Detección.

Repite el ciclo 3 veces y promedia para obtener MTTD/MTTR promedio.

## Seguridad implementada

- Validación: usuario `[A-Za-z0-9_]{4,20}`, correo con regex, contraseña ≥ 8.
- Normalización con `strip()` + `.get()`.
- Hash con `generate_password_hash` / `check_password_hash` (scrypt, no texto plano).
- Consultas parametrizadas con `?` (resistente a inyección SQL).
- Detección de duplicados (`usuario` o `correo` ya registrado).
- Registro de eventos en `eventos.log` y respuesta simulada en `respuesta.log`.
