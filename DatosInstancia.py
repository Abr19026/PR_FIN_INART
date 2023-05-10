from collections import defaultdict

# Guarda la información de cada actividad
class Actividad:
    __slots__ = ("num_act", "subtema", "tiempo", "valor", "obligatoria", "requiere")
    def __init__(self, num_act, subtema, tiempo, valor, obligatorio, requiere) -> None:
        self.num_act: int = int(num_act)
        self.subtema: int = int(subtema)    # Subtema al que pertenece la actividad
        self.tiempo: float = tiempo         # Tiempo que toma la actividad
        self.valor: float = valor           # Valor que contribuye la actividad
        self.obligatoria: bool = bool(obligatorio)  # True si es obligatoria, False si no
        self.requiere: set[int] = requiere  # Set con los numeros de actividad de las que depende la actividada actual

    def __str__(self) -> str:
        return f"subtema: {self.subtema}, tiempo: {self.tiempo}, valor: {self.valor}, oblig: {self.obligatoria}, reqs: {self.requiere}"

# Guarda los numeros de las actividades de cada subtema
# y la calificación mímima restante
class DatosSubtema:
    __slots__ = ("nums_actividades", "valor_min")
    
    def __init__(self, valor_min) -> None:
        self.nums_actividades: set[int] = set()
        self.valor_min: float = valor_min

# Guarda todas las actividades en .actividades
# Guarda los datos de cada subtema en .subtemas
class Instancia_Pl_Ed:
    __slots__ = ("actividades", "subtemas", "kmin")
    
    def __init__(self, kmin: float) -> None:
        self.kmin = kmin
        self.actividades: dict[int, Actividad] = {}
        self.subtemas: dict[int, DatosSubtema] = {} #defaultdict(DatosSubtema)
        #self.arbol_inv_deps = 
    
    def add_actividad(self, actividad: Actividad):
        num = actividad.num_act
        self.actividades[num] = actividad
        if actividad.subtema in self.subtemas:
            self.subtemas[actividad.subtema].nums_actividades.add(num)
        else:
            self.subtemas[actividad.subtema] = DatosSubtema(self.kmin)

    def __str__(self) -> str:
        retorno = ""
        for subtema in sorted(self.subtemas.keys()):
            for num_actividad in sorted(self.subtemas[subtema].nums_actividades):
                retorno += f"{num_actividad}: {self.actividades[num_actividad]}\n"
        return retorno
    
carpeta_instancias = "instancias"

# Crea una instancia del problema dado el nombre de un archivo
# y una calificación mínima kmin para todos los subtemas
def get_problema(nombre_archivo: str, kmin: float) -> Instancia_Pl_Ed:
    with open(f"{carpeta_instancias}/{nombre_archivo}") as archivo:
        instancia = Instancia_Pl_Ed(kmin)
        
        for linea in archivo.readlines():
            lista_act = list(map(float, linea.split(',')))
            num_act = int(lista_act[3])
            subtema = lista_act[2]
            tiempo = lista_act[4]
            valor = lista_act[5]
            obligatorio = lista_act[9]
            reqs = set()
            for i in range(7, 9):
                if lista_act[i] > 0:
                    reqs.add(int(lista_act[i]))
            
            nueva_act = Actividad(num_act, subtema , tiempo, valor, obligatorio, reqs)
            instancia.add_actividad(nueva_act)
        return instancia
    


