from DatosInstancia import Actividad, DatosSubtema, Instancia_Pl_Ed

# Dada una instancia y un número de actividad retorna un plan
# que resuelve sus dependencias en orden (wrapper de GetDependencias)
def ResolverDependencias(instancia: Instancia_Pl_Ed, num_activ: int) -> list[int]:
    lista_plan = []
    GetDependencias(instancia, [num_activ], lista_plan)
    return lista_plan

# Dada una Pila con un elemento (pila camina), 
# obtiene el plan (Lista ordenada) que resuelve todas sus dependencias en orden
def GetDependencias(instancia: Instancia_Pl_Ed, pila_camino: list[int], Plan: list):
    if len(pila_camino) > 0:
        for dependencia in instancia.actividades[pila_camino[-1]].requerimientos:
            if dependencia in pila_camino:
                raise Exception("Ciclo en dependencias")
            elif dependencia in Plan:
                continue
            else:
                pila_camino.append(dependencia)
                GetDependencias(instancia, pila_camino, Plan)
        Plan.append(pila_camino.pop())
    return