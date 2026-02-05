# 📚 Tutorial Completo: Habit Tracker desde Cero

**Aprende a crear una aplicación web moderna de gestión de hábitos con Python y Flask**


## Introducción

### ¿Qué vamos a construir?

Una aplicación web completa para:
-  Gestionar hábitos diarios
-  Ver rachas de cumplimiento
-  Planificar objetivos semanales
-  Escribir reflexiones
-  Ver historial completo

### Tecnologías utilizadas

- **Python 3.8+**: Lenguaje de programación
- **Flask**: Framework web minimalista
- **JSON**: Almacenamiento de datos

---

## Requisitos Previos

### Conocimientos Necesarios

- ✅ Python básico (variables, funciones, clases)
- ✅ HTML básico (etiquetas, formularios)
- ✅ CSS básico (colores, layouts)

### Software Necesario

```bash
# Verificar Python
python --version  # Debe ser 3.8 o superior

# Instalar Flask
pip install flask
```

---

## Conceptos Básicos

### ¿Qué es Flask?

Flask es un **micro-framework web** para Python. Piensa en él como una herramienta que:
- Convierte funciones Python en páginas web
- Maneja solicitudes HTTP (GET, POST)
- Renderiza plantillas HTML
- Gestiona sesiones de usuario

**Ejemplo mínimo:**
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "¡Hola Mundo!"

app.run()
```

### Conceptos Clave

| Concepto | Explicación | Ejemplo |
|----------|-------------|---------|
| **Ruta** | URL que el usuario visita | `/login`, `/habitos` |
| **Vista** | Función que maneja una ruta | `def login():` |
| **Template** | Archivo HTML con variables | `login.html` |
| **Sesión** | Memoria del usuario | Recordar quién está logueado |

---

## Paso 1: Modelos de Datos

### ¿Qué son los Modelos?

Los modelos son **clases Python que representan datos**. Son como planos para crear objetos.

### Archivo: `objetos.py`

#### Modelo: Habito

```python
import datetime

class Habito:
    """Representa un hábito que quieres seguir diariamente"""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.fechas_completadas: set[datetime.date] = set()
    
    def completar_hoy(self) -> None:
        hoy = datetime.date.today()
        self.fechas_completadas.add(hoy)
    
    def esta_completado_hoy(self) -> bool:
        hoy = datetime.date.today()
        return hoy in self.fechas_completadas
```

Usamos set porque al hashear aumenta mucho el rendimiento y no acepta duplicados.

#### Racha con Día de Gracia

```python
def racha_actual(self) -> int:
    """
    Calcula cuántos días consecutivos has completado el hábito.
    
    if not self.fechas_completadas:
        return 0
    
    hoy = datetime.date.today()
    ayer = hoy - datetime.timedelta(days=1)
    
    # Si no completaste ni hoy ni ayer, racha rota
    if hoy not in self.fechas_completadas and ayer not in self.fechas_completadas:
        return 0
    
    # Comenzar desde el día más reciente
    dia_inicio = hoy if hoy in self.fechas_completadas else ayer
    
    racha = 0
    dia = dia_inicio
    while dia in self.fechas_completadas:
        racha += 1
        dia = dia - datetime.timedelta(days=1)
    
    return racha
```

---

## Paso 2: Configurar Flask

```python
from flask import Flask, render_template, request, redirect, session, flash
from objetos import Usuario

app = Flask(__name__)
app.secret_key = "habit-tracker-2026-super-segura"

usuarios = {}
```

---

## Paso 3: Sistema de Autenticación

### Función Helper de Seguridad

```python
def obtener_usuario_actual():
    if "usuario" not in session:
        return None
    
    nombre_usuario = session["usuario"]
    
    if nombre_usuario not in usuarios:
        session.clear()
        return None
    
    return usuarios[nombre_usuario]
```

### Ruta de Login

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario" in session and session["usuario"] not in usuarios:
        session.clear()
        flash("Tu sesión anterior ha expirado", "info")
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        contraseña = request.form.get("contraseña", "").strip()
        
        if nombre in usuarios and usuarios[nombre]._contraseña == contraseña:
            session["usuario"] = nombre
            flash("¡Bienvenido de nuevo!", "success")
            return redirect("/habitos")
        
        flash("Usuario o contraseña incorrectos", "error")
    
    return render_template("login.html")
```

---

## Paso 7: Persistencia de Datos

### Guardar Datos

```python
def guardar_usuarios():
    data = {}
    for nombre, usuario in usuarios.items():
        data[nombre] = {
            "contraseña": usuario._contraseña,
            "habitos": {
                h.nombre: [f.isoformat() for f in h.fechas_completadas] 
                for h in usuario.habitos.values()
            },
            "semanas": [...]
        }
    
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```
