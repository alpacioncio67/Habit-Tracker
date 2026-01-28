# Habit-Tracker
Pequeño proyecto web que te ayuda a llevar cuenta tanto de tus hábitos diarios como de tus objetivos semanales.

STACK DE TECNOLOGÍAS (flask)

Frontend (navegador)
    ↓ HTTP/JSON
Flask (servidor Python)
    ├─ Routes (controladores)
    ├─ Templates (Jinja2)
    └─ Static (CSS/JS)
    ↓ SQL
SQLAlchemy ORM (mapea clases Python → BD)
    ↓
SQLite (base de datos)

ESTRUCTURA DE CARPETAS

habit_tracker/
├── app.py                    (Servidor Flask principal)
├── models.py                 (SQLAlchemy ORM)
├── requirements.txt          (Dependencias)
├── instance/
│   └── app.db               (SQLite - se crea automáticamente)
├── static/
│   ├── style.css            (Estilos)
│   └── script.js            (JavaScript)
└── templates/
    ├── base.html            (Layout base)
    ├── index.html           (Home)
    ├── login.html           (Autenticación)
    └── dashboard.html       (Panel principal)



