from DatosInstancia import get_problema
from planeacion import ResolverDependencias

archivos = [
"f_1_0.csv", "f_1_1.csv", "f_1_2.csv", "f_2_0.csv", "f_2_1.csv", "f_2_2.csv", 
"f_3_0.csv", "f_3_1.csv", "f_3_2.csv", "f_4_0.csv", "f_4_1.csv", "f_4_2.csv", 
"f_5_0.csv", "f_5_1.csv", "f_5_2.csv", "i_1_0.csv", "i_1_1.csv", "i_1_2.csv", 
"i_2_0.csv", "i_2_1.csv", "i_2_2.csv", "i_3_0.csv", "i_3_1.csv", "i_3_2.csv", 
"i_4_0.csv", "i_4_1.csv", "i_4_2.csv", "i_5_0.csv", "i_5_1.csv", "i_5_2.csv"]

carpetaInstancias = "./instancias"
archivo_a_leer = f"{carpetaInstancias}/{archivos[29]}"

inst = get_problema(archivo_a_leer, 70)
print(inst)
print("resolución de dependencias")
for i in inst.actividades:
    print(f"{i}: {ResolverDependencias(inst, i, set())}")