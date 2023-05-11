from DatosInstancia import get_problema
from planeacion import CrearPlan

Archivos_instancias = [
"f_1_0.csv", "f_1_1.csv", "f_1_2.csv", "f_2_0.csv", "f_2_1.csv", "f_2_2.csv", 
"f_3_0.csv", "f_3_1.csv", "f_3_2.csv", "f_4_0.csv", "f_4_1.csv", "f_4_2.csv", 
"f_5_0.csv", "f_5_1.csv", "f_5_2.csv", "i_1_0.csv", "i_1_1.csv", "i_1_2.csv", 
"i_2_0.csv", "i_2_1.csv", "i_2_2.csv", "i_3_0.csv", "i_3_1.csv", "i_3_2.csv", 
"i_4_0.csv", "i_4_1.csv", "i_4_2.csv", "i_5_0.csv", "i_5_1.csv", "i_5_2.csv"]

archivos_prueba = [Archivos_instancias[14]]

carpetaInstancias = "./instancias"
calif_minima = 70

for archivo in archivos_prueba:
    archivo_a_leer = f"{carpetaInstancias}/{archivo}"
    inst = get_problema(archivo_a_leer, calif_minima)
    print(inst)
    plan = CrearPlan(inst)
    print(f":::Plan::: {plan}")