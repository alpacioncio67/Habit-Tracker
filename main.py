from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
import datetime
from objetos import Usuario

app = Flask(__name__)
app.secret_key = "habit-tracker-2026-super-segura"

usuarios = {}

def guardar_usuarios():
    """Guarda todos los usuarios en un archivo JSON"""
    data = {}
    for nombre, usuario in usuarios.items():
        data[nombre] = {
            "contraseña": usuario._contraseña,
            "habitos": {h.nombre: [f.isoformat() for f in h.fechas_completadas] for h in usuario.habitos.values()},
            "semanas": [{"fecha_inicio": s.fecha_inicio.isoformat(), 
                        "objetivos": s.objetivos,
                        "completados": s.objetivos_completados,
                        "reflexion": getattr(s, 'reflexion', '')} for s in usuario.semanas]
        }
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def cargar_usuarios():
    """Carga los usuarios desde el archivo JSON al iniciar"""
    global usuarios
    try:
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", encoding="utf-8") as f:
                data = json.load(f)
            for nombre, info in data.items():
                u = Usuario(nombre, info.get("contraseña", ""))
                for h_nombre, fechas_str in info.get("habitos", {}).items():
                    try:
                        h = u.crear_habito(h_nombre)
                        h.fechas_completadas = {datetime.date.fromisoformat(f) for f in fechas_str}
                    except: 
                        pass
                for s_data in info.get("semanas", []):
                    try:
                        s = u.crear_semana(s_data["objetivos"])
                        s.fecha_inicio = datetime.date.fromisoformat(s_data["fecha_inicio"])
                        s.objetivos_completados = s_data["completados"]
                        s.reflexion = s_data.get("reflexion", "")
                    except: 
                        pass
                usuarios[nombre] = u
    except Exception as e:
        print(f"Error cargando usuarios: {e}")

cargar_usuarios()

@app.route("/")
def home():
    if "usuario" in session:
        return redirect("/habitos")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        contraseña = request.form.get("contraseña", "").strip()
        if nombre in usuarios and usuarios[nombre]._contraseña == contraseña:
            session["usuario"] = nombre
            flash("¡Bienvenido de nuevo!", "success")
            return redirect("/habitos")
        flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")

@app.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        contraseña = request.form.get("contraseña", "").strip()
        if nombre and contraseña and nombre not in usuarios:
            usuarios[nombre] = Usuario(nombre, contraseña)
            guardar_usuarios()
            flash("¡Cuenta creada exitosamente!", "success")
            return redirect("/login")
        flash("Error: usuario ya existe o campos vacíos", "error")
    return render_template("crear.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect("/login")

@app.route("/cuenta/eliminar", methods=["POST"])
def eliminar_cuenta():
    """Permite al usuario eliminar su propia cuenta"""
    if "usuario" not in session:
        return redirect("/login")
    
    nombre = session["usuario"]
    confirmacion = request.form.get("confirmacion", "").strip()
    
    if confirmacion == nombre:
        usuarios.pop(nombre, None)
        guardar_usuarios()
        session.clear()
        flash(f"Cuenta '{nombre}' eliminada correctamente", "info")
        return redirect("/login")
    else:
        flash("Confirmación incorrecta. Debes escribir tu nombre de usuario", "error")
        return redirect("/habitos")

@app.route("/habitos")
def habitos():
    if "usuario" not in session: 
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    return render_template("habitos.html", usuario=usuario)

@app.route("/semanas")
def semanas():
    if "usuario" not in session: 
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    return render_template("semanas.html", usuario=usuario)

# ===== RUTAS DE HÁBITOS =====

@app.route("/habito/nuevo", methods=["POST"])
def habito_nuevo():
    if "usuario" not in session:
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    try:
        nombre = request.form.get("nombre", "").strip()
        if nombre:
            usuario.crear_habito(nombre)
            guardar_usuarios()
            flash(f"✅ Hábito '{nombre}' creado", "success")
        else:
            flash("El nombre del hábito no puede estar vacío", "error")
    except ValueError as e:
        flash(f"❌ {e}", "error")
    return redirect("/habitos")

@app.route("/habito/completar", methods=["POST"])
def habito_completar():
    if "usuario" not in session:
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    nombre = request.form.get("nombre", "").strip()
    h = usuario.obtener_habito(nombre)
    if h:
        h.completar_hoy()
        guardar_usuarios()
        flash(f"✅ '{nombre}' completado hoy", "success")
    else:
        flash("Hábito no encontrado", "error")
    return redirect("/habitos")

@app.route("/habito/eliminar", methods=["POST"])
def habito_eliminar():
    if "usuario" not in session:
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    nombre = request.form.get("nombre", "").strip()
    usuario.eliminar_habito(nombre)
    guardar_usuarios()
    flash(f"🗑️ Hábito '{nombre}' eliminado", "info")
    return redirect("/habitos")

# ===== RUTAS DE SEMANAS =====

@app.route("/semana/nueva", methods=["POST"])
def semana_nueva():
    if "usuario" not in session:
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    objetivos_texto = request.form.get("objetivos", "")
    objetivos = [o.strip() for o in objetivos_texto.splitlines() if o.strip()]
    usuario.crear_semana(objetivos)
    guardar_usuarios()
    flash("📅 Nueva semana creada", "success")
    return redirect("/semanas")

@app.route("/semana/objetivo/nuevo", methods=["POST"])
def semana_objetivo_nuevo():
    if "usuario" not in session:
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    semana = usuario.ultima_semana()
    if not semana:
        flash("No hay semana creada", "error")
        return redirect("/semanas")
    
    objetivo = request.form.get("objetivo", "").strip()
    if objetivo:
        semana.añadir_objetivo(objetivo)
        guardar_usuarios()
        flash("➕ Objetivo añadido", "success")
    return redirect("/semanas")

@app.route("/semana/objetivo/completar", methods=["POST"])
def semana_objetivo_completar():
    if "usuario" not in session:
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    semana = usuario.ultima_semana()
    if not semana:
        flash("No hay semana creada", "error")
        return redirect("/semanas")
    
    objetivo = request.form.get("objetivo", "").strip()
    if objetivo:
        semana.completar_objetivo(objetivo)
        guardar_usuarios()
        flash("✅ Objetivo completado", "success")
    return redirect("/semanas")

@app.route("/semana/reflexion", methods=["POST"])
def semana_reflexion():
    if "usuario" not in session:
        return redirect("/login")
    usuario = usuarios[session["usuario"]]
    semana = usuario.ultima_semana()
    if not semana:
        flash("No hay semana creada", "error")
        return redirect("/semanas")
    
    reflexion = request.form.get("reflexion", "").strip()
    semana.establecer_reflexion(reflexion)
    guardar_usuarios()
    flash("💾 Reflexión guardada", "success")
    return redirect("/semanas")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
