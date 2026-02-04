import os
if os.path.exists("usuarios.json"):
    os.remove("usuarios.json")
    print("✅ Datos eliminados")
