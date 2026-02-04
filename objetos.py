# habit_tracker/models.py
import datetime


class Habito:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.fechas_completadas: set[datetime.date] = set()

    def completar_hoy(self) -> None:
        hoy = datetime.date.today()
        self.fechas_completadas.add(hoy)

    def esta_completado_hoy(self) -> bool:
        hoy = datetime.date.today()
        return hoy in self.fechas_completadas

def racha_actual(self) -> int:
    if not self.fechas_completadas:
        return 0
    
    hoy = datetime.date.today()
    ayer = hoy - datetime.timedelta(days=1)
    
    # ✅ Racha continúa si completaste hoy O ayer
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

    def mejor_racha(self) -> int:
        if not self.fechas_completadas:
            return 0
        dias = sorted(self.fechas_completadas)
        mejor = 1
        actual = 1
        for i in range(1, len(dias)):
            if dias[i] == dias[i - 1] + datetime.timedelta(days=1):
                actual += 1
            else:
                mejor = max(mejor, actual)
                actual = 1
        mejor = max(mejor, actual)
        return mejor

    def __str__(self) -> str:
        estado = "✔" if self.esta_completado_hoy() else "✘"
        return (f"Hábito: {self.nombre} | Hoy: {estado} | "
                f"Racha actual: {self.racha_actual()} | "
                f"Mejor racha: {self.mejor_racha()}")


class Usuario:
    def __init__(self, nombre: str, contraseña: str):
        self.nombre = nombre
        self._contraseña = contraseña
        self.habitos: dict[str, Habito] = {}
        self.semanas: list[Semana] = []  # adelantamos el tipo con string si hace falta

    def crear_habito(self, nombre_habito: str) -> Habito:
        if nombre_habito in self.habitos:
            raise ValueError("El hábito ya existe")
        habito = Habito(nombre_habito)
        self.habitos[nombre_habito] = habito
        return habito

    def obtener_habito(self, nombre_habito: str) -> Habito | None:
        return self.habitos.get(nombre_habito)

    def eliminar_habito(self, nombre_habito: str) -> None:
        self.habitos.pop(nombre_habito, None)

    def listar_habitos(self) -> list[Habito]:
        return list(self.habitos.values())

    def crear_semana(self, objetivos: list[str] | None = None) -> "Semana":
        semana = Semana(objetivos)
        self.semanas.append(semana)
        return semana

    def ultima_semana(self) -> "Semana | None":
        if not self.semanas:
            return None
        return self.semanas[-1]


class Semana:
    def __init__(self, objetivos: list[str] | None = None):
        self.fecha_inicio = datetime.date.today()
        self.objetivos: list[str] = objetivos or []
        self.objetivos_completados: list[str] = []
        self.reflexion: str = ""

    def añadir_objetivo(self, objetivo: str) -> None:
        if objetivo not in self.objetivos:
            self.objetivos.append(objetivo)

    def completar_objetivo(self, objetivo: str) -> None:
        if objetivo in self.objetivos and objetivo not in self.objetivos_completados:
            self.objetivos_completados.append(objetivo)

    def establecer_reflexion(self, texto: str) -> None:
        self.reflexion = texto

    def progreso(self) -> float:
        if not self.objetivos:
            return 0.0
        return len(self.objetivos_completados) / len(self.objetivos)

    def __str__(self) -> str:
        prog = self.progreso() * 100
        return (f"Semana iniciada el {self.fecha_inicio} | "
                f"Objetivos: {len(self.objetivos)} | "
                f"Completados: {len(self.objetivos_completados)} | "
                f"Progreso: {prog:.1f}%")
