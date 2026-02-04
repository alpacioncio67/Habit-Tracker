# 🎯 Habit Tracker - Gestor de Hábitos y Objetivos

Una aplicación web moderna y minimalista para gestionar tus hábitos diarios y objetivos semanales. Construida con Python y Flask.

##  Características

### Gestión de Hábitos
-  Crear hábitos personalizados
-  Sistema de rachas con día de gracia
-  Marcar hábitos como completados
-  Visualizar racha actual y mejor racha
-  Eliminar hábitos

### Gestión de Semanas
-  Crear objetivos semanales
-  Marcar objetivos completados
-  Añadir objetivos sobre la marcha
-  Barra de progreso visual
-  Escribir reflexiones semanales

### Características Técnicas
-  Sistema de autenticación
-  Persistencia automática de datos (JSON)
-  Diseño responsivo
-  Interfaz moderna con gradientes
-  Sin autocompletado (mayor privacidad)
-  Eliminar cuenta cuando quieras

---

## 🔧 Requisitos

- **Python 3.8+**
- **Flask 3.0+**

---

##  Instalación

### 1. Instalar Flask

```bash
pip install flask
```

### 2. Ejecutar la aplicación

```bash
python main.py
```

### 3. Abrir en el navegador

```
http://localhost:5000
```

---

##  Uso

### Primera Vez

1. Abre `http://localhost:5000`
2. Haz clic en "Créala aquí"
3. Ingresa nombre de usuario y contraseña
4. ¡Empieza a crear hábitos!


## 📁 Estructura del Proyecto

```
habit-tracker/
│
├── main.py                 # Servidor Flask (rutas y lógica)
├── objetos.py              # Modelos (Usuario, Habito, Semana)
├── usuarios.json           # Base de datos (se crea automáticamente)
│
├── templates/              # Plantillas HTML
│   ├── base.html          # Plantilla base con CSS
│   ├── login.html         # Inicio de sesión
│   ├── crear.html         # Registro
│   ├── habitos.html       # Gestión de hábitos
│   └── semanas.html       # Gestión de semanas
│
├── README.md              # Este archivo
├── TUTORIAL.md            # Tutorial paso a paso
└── MODIFICACIONES.md      # Guía de modificaciones
```

---

##  Funcionalidades Detalladas

### Sistema de Rachas

Las rachas muestran cuántos días **consecutivos** has completado un hábito.

**Día de gracia:**
- ✅ Completaste **hoy** → Racha continúa
- ✅ Completaste **ayer** → Racha continúa (1 día de gracia)
- ❌ No completaste ni hoy ni ayer → Racha se reinicia a 0

**Ejemplo:**
```
Lunes:     ✅ → Racha: 1
Martes:    ✅ → Racha: 2
Miércoles: ❌ → Racha: 2 (día de gracia)
Jueves:    ✅ → Racha: 3
Viernes:   ❌ → Racha: 3 (día de gracia)
Sábado:    ❌ → Racha: 0 (pasaron 2 días)
```

### Gestión de Cuenta

Para eliminar tu cuenta:

1. Ve a "⚙️ Cuenta" en la navegación
2. Escribe tu nombre de usuario exacto
3. Haz clic en "Eliminar cuenta"

 **Esta acción es irreversible**

---

##  Gestión de Datos

### Dónde se Guardan los Datos

Todo se guarda en `usuarios.json` en formato JSON.


### Borrar TODOS los Datos

Script reset.py


##  Mejoras Futuras

Ideas para extender el proyecto:

- [ ] Gráficos de progreso (Chart.js)
- [ ] Exportar a PDF/CSV
- [ ] Categorías de hábitos
- [ ] Recordatorios por email
- [ ] Tema oscuro
- [ ] Estadísticas mensuales
- [ ] App móvil
- [ ] Base de datos SQL

---

##  Seguridad

 **Este proyecto es educativo y para uso local.**

---

##  Recursos

- `TUTORIAL.md` - Tutorial detallado de la creación del proyecto
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python datetime](https://docs.python.org/3/library/datetime.html)

---

##  Licencia

MIT License - Libre para usar, modificar y distribuir

---




