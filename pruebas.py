from DatosInstancia import get_problema, Instancia_Pl_Ed
from planeacion import CrearPlan
from copy import deepcopy
from dataclasses import dataclass, asdict
from timeit import *
import pandas as pd

carpetaInstancias = "./instancias"
Archivos_instancias = [
"f_1_0.csv", "f_1_1.csv", "f_1_2.csv", "f_2_0.csv", "f_2_1.csv", "f_2_2.csv", 
"f_3_0.csv", "f_3_1.csv", "f_3_2.csv", "f_4_0.csv", "f_4_1.csv", "f_4_2.csv", 
"f_5_0.csv", "f_5_1.csv", "f_5_2.csv", "i_1_0.csv", "i_1_1.csv", "i_1_2.csv", 
"i_2_0.csv", "i_2_1.csv", "i_2_2.csv", "i_3_0.csv", "i_3_1.csv", "i_3_2.csv", 
"i_4_0.csv", "i_4_1.csv", "i_4_2.csv", "i_5_0.csv", "i_5_1.csv", "i_5_2.csv"]

archivos_prueba = Archivos_instancias
calif_minima = 60

def validar_solucion(solucion: list[list[int]], inst: Instancia_Pl_Ed):
    hasta_ahora = set()
    tiempo_total = 0
    califs_subtemas = {}
    for subtema in inst.subtemas:
        califs_subtemas[subtema] = 0
    
    # Valida dependencias
    for actividad in solucion:
        if actividad in hasta_ahora:
            return (False, f"Se repite: {actividad}")
        datos_act = inst.actividades[actividad]
        if not hasta_ahora.issuperset(datos_act.requiere):
            return (False, f"sin requisitos: {actividad}")
        hasta_ahora.add(actividad)
        tiempo_total += datos_act.tiempo
        califs_subtemas[datos_act.subtema] += datos_act.valor
    
    # Valida calificaciones
    for subtema in inst.subtemas:
        if califs_subtemas[subtema] < inst.subtemas[subtema].calif_min:
            return  (False, f"calificacion baja: {subtema}")
        
    return (True, tiempo_total, califs_subtemas)

@dataclass
class Resultados:
    archivo: str
    tiempo_ejecucion: float
    duracion_plan: float
    solucion: list
    calificaciones_subtemas: dict

lista_soluciones = []

for archivo in archivos_prueba:
    archivo_a_leer = f"{carpetaInstancias}/{archivo}"
    inst = get_problema(archivo_a_leer, calif_minima)
    inst_pruebas = deepcopy(inst)
    
    t_0 = default_timer()
    plan, duracion = CrearPlan(inst)
    tiempo_ejecucion = round(default_timer() - t_0, 6)
    plan_procesado = plan[0] + plan[1]
    validacion = validar_solucion(plan_procesado, inst_pruebas)
    lista_soluciones.append(asdict(Resultados(archivo,tiempo_ejecucion, duracion, plan_procesado, validacion[2])))
    if validacion[0] == False:
        raise Exception(f"error en archivo {archivo}")
df = pd.DataFrame(lista_soluciones)
print(df)

with open(f"./Resultados/{calif_minima}.csv","w") as arch_salida:
    df.to_csv(arch_salida)