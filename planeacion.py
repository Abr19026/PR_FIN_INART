from DatosInstancia import Actividad, DatosSubtema, Instancia_Pl_Ed
from itertools import product

class Posible_solucion:
    __slots__ = ("activs", "tiempo", "calif")
    def __init__(self) -> None:
        self.activs: set[int] = set()
        self.tiempo: float = 0
        self.calif: float = 0

def sol_voraz_calif(inst: Instancia_Pl_Ed, num_subt: int, calif_objetivo):
    sol = Posible_solucion()
    for num_activ in sorted(inst.get_actividades(num_subt), key=lambda x: inst.actividades[x].valor, reverse=True):
        if sol.calif < calif_objetivo:
            activ = inst.actividades[num_activ]
            sol.activs.add(num_activ)
            sol.calif += activ.valor
            sol.tiempo += activ.tiempo
        else:
            return sol
    raise Exception(f"El subtema {num_subt} no tiene las actividades suficientes para cumplir calificación objetivo")

def sol_voraz_tiempo(inst: Instancia_Pl_Ed, num_subt: int, calif_objetivo):
    sol = Posible_solucion()
    for num_activ in sorted(inst.get_actividades(num_subt), key=lambda x: inst.actividades[x].tiempo):
        if sol.calif < calif_objetivo:
            activ = inst.actividades[num_activ]
            sol.activs.add(num_activ)
            sol.calif += activ.valor
            sol.tiempo += activ.tiempo
        else:
            return sol
    raise Exception(f"El subtema {num_subt} no tiene las actividades suficientes para cumplir calificación objetivo")

def sol_voraz_densidad(inst: Instancia_Pl_Ed, num_subt: int, calif_objetivo):
    sol = Posible_solucion()
    for num_activ in sorted(inst.get_actividades(num_subt), key=lambda x: inst.actividades[x].tiempo/inst.actividades[x].valor):
        if sol.calif < calif_objetivo:
            activ = inst.actividades[num_activ]
            sol.activs.add(num_activ)
            sol.calif += activ.valor
            sol.tiempo += activ.tiempo
        else:
            return sol
    raise Exception(f"El subtema {num_subt} no tiene las actividades suficientes para cumplir calificación objetivo")


class ListaCombsSols:
    __slots__ = ("inst", "combs_sols")
    funcs_sols = (sol_voraz_calif, sol_voraz_tiempo, sol_voraz_densidad)
    def __init__(self, inst: Instancia_Pl_Ed) -> None:
        self.inst: Instancia_Pl_Ed = inst
        self.combs_sols: dict[int, list[Posible_solucion]] = {}
        
        for subtem in inst.subtemas:
            calif_min = inst.subtemas[subtem].calif_min
            lista_sols = [func(inst, subtem, calif_min) for func in self.funcs_sols]
            lista_sols.sort(key=lambda x: x.tiempo)
            self.combs_sols[subtem] = lista_sols

def get_producto_sols_posibles(Lista_sols: ListaCombsSols):
    for producto in product(*[Lista_sols.combs_sols[x] for x in Lista_sols.combs_sols]):
        escogidos = set()
        tiempo = 0
        plan = []
        for sol_subtema in producto:
            for activ in sol_subtema.activs:
                plan.extend(ResolverDependencias(Lista_sols.inst, activ, escogidos))
        for activ in plan:
            tiempo += Lista_sols.inst.actividades[activ].tiempo
        yield (plan, tiempo)
# (wrapper de GetDependencias)
# Dada una instancia y un número de actividad retorna un plan que resuelve sus dependencias en orden 
# además actualiza un conjunto que guarde las dependencias resueltas
def ResolverDependencias(instancia: Instancia_Pl_Ed, num_activ: int, deps_resueltas: set[int]) -> list[int]:
    lista_plan = []
    GetDependencias(instancia, [num_activ], lista_plan, deps_resueltas)
    return lista_plan

# Dada una Pila con un elemento (pila camina), 
# obtiene el plan (Lista ordenada) que resuelve todas sus dependencias en orden
def GetDependencias(instancia: Instancia_Pl_Ed, pila_camino: list[int], Plan: list, resueltas: set[int]):
    if len(pila_camino) > 0:
        for dependencia in instancia.actividades[pila_camino[-1]].requiere:
            if dependencia in pila_camino:
                raise Exception("Ciclo en dependencias")
            elif dependencia in resueltas:
                continue
            else:
                pila_camino.append(dependencia)
                GetDependencias(instancia, pila_camino, Plan, resueltas)
        actividad_agregar = pila_camino.pop()
        long_anterior = len(resueltas)
        resueltas.add(actividad_agregar)
        if long_anterior != len(resueltas):
            Plan.append(actividad_agregar)
    return

def CrearPlan(inst: Instancia_Pl_Ed) -> tuple[list, float]:
    tiempo = 0
    plan: list[list[Actividad] | set[Actividad]] = [] # Plan a retornar
    escogidos: set[int] = set() # Guarda los índices de las actividades ya escogidas
    # Primero escoge las obligatorias
    plan_obligs = []
    for num_act, actividad in inst.actividades.items():
        if actividad.obligatoria:
            plan_deps = ResolverDependencias(inst, num_act, escogidos)
            plan_obligs.extend(plan_deps)
    plan.append(plan_obligs)
    # Actualiza valores de la instancia
    for num_act in plan_obligs:
        # Actualiza datos del subtema
        subtema_act = inst.get_subtema(num_act)
        subtema_act.nums_actividades.remove(num_act)
        subtema_act.calif_min -= inst.actividades[num_act].valor
        # Actualiza datos del plan
        actividad_actual = inst.actividades[num_act]
        tiempo += actividad_actual.tiempo
        # Elimina dependencias ya resueltas
        for requerido_por in actividad_actual.requerido_por:
            inst.actividades[requerido_por].requiere.remove(num_act)
    
    
    # La instancia se tratará de ahora en adelante como si nunca
    # hubiera tenido las actividades obligatorias
    posibles_sols = ListaCombsSols(inst)
    mejor_tiempo = float("inf")
    mejor_resto_plan = []
    for resto_plan, tiempo_resto in get_producto_sols_posibles(posibles_sols):
        if tiempo_resto < mejor_tiempo:
            mejor_resto_plan = resto_plan
            mejor_tiempo = tiempo_resto
    plan.append(mejor_resto_plan)
    tiempo += mejor_tiempo
    return (plan, tiempo)