from collections import defaultdict

# Guarda la información de cada actividad
class Actividad:
    __slots__ = ("subtema", "tiempo", "valor", "obligatoria", "requerimientos")
    def __init__(self, subtema, tiempo, valor, obligatorio, requerimientos) -> None:
        self.subtema: int = int(subtema)    # Subtema al que pertenece la actividad
        self.tiempo: float = tiempo         # Tiempo que toma la actividad
        self.valor: float = valor           # Valor que contribuye la actividad
        self.obligatoria: bool = bool(obligatorio)  # True si es obligatoria, False si no
        self.requerimientos: set[int] = requerimientos  # Set con los numeros de actividad de las que depende la actividada actual

    def __str__(self) -> str:
        return f"subtema: {self.subtema}, tiempo: {self.tiempo}, valor: {self.valor}, oblig: {self.obligatoria}, reqs: {self.requerimientos}"

# Guarda todas las actividades en .actividades
# Guarda los numeros de las actividades que pertenecen a cada subtema en .subtemas
class Instancia_Pl_Ed:
    __slots__ = ("actividades", "subtemas")
    
    def __init__(self) -> None:
        self.subtemas: dict[int, set[int]] = defaultdict(set)
        self.actividades: dict[int,Actividad] = {}
    
    def __str__(self) -> str:
        retorno = ""
        for subtema in sorted(self.subtemas):
            for num_actividad in sorted(self.subtemas[subtema]):
                retorno += f"{num_actividad}: {self.actividades[num_actividad]}\n"
        return retorno
    
carpeta_instancias = "instancias"

#Crea una instancia del problema dado el nombre de un archivo
def get_problema(nombre_archivo: str) -> Instancia_Pl_Ed:
    with open(f"{carpeta_instancias}/{nombre_archivo}") as archivo:
        instancia = Instancia_Pl_Ed()
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
                    reqs.add(int(lista_act[i] - 1))
            
            nueva_act = Actividad(subtema , tiempo, valor, obligatorio, reqs)

            instancia.actividades[num_act] = nueva_act
            instancia.subtemas[subtema].add(num_act)
        return instancia
    
if __name__ == "__main__":
    inst = get_problema("f_5_2.csv")
    print(inst)

