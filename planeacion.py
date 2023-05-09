
def GetDependencias(pila_camino: list, Plan: list):
    for dependencia in pila_camino[-1].dependencias():
        if dependencia in pila_camino:
            raise Exception("Ciclo en dependencias")
        elif dependencia in Plan:
            continue
        else:
            pila_camino.append(dependencia)
            GetDependencias(pila_camino, Plan)
    Plan.append(pila_camino.pop())