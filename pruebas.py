from DatosInstancia import get_problema
from planeacion import ResolverDependencias



inst = get_problema("f_5_2.csv", 70)
print(inst)
print("resolución de dependencias")
for i in inst.actividades:
    print(f"{i}: {ResolverDependencias(inst, i, set())}")