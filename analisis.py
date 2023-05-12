import pandas as pd
import matplotlib.pyplot as plt

resultado_60 = pd.read_csv("Resultados/60.csv")
resultado_70 = pd.read_csv("Resultados/70.csv")
resultado_80 = pd.read_csv("Resultados/80.csv")
resultado_90 = pd.read_csv("Resultados/90.csv")
lista_resultados = [resultado_60,resultado_70,resultado_80,resultado_90]

resultados_tiempo_ejecucion = pd.concat([lista_resultados[0]["archivo"]] + [x["tiempo_ejecucion"] for x in lista_resultados], 
                                        axis=1, 
                                        keys=["instancia", "60", "70", "80", "90"])

resultados_duracion_plan = pd.concat([lista_resultados[0]["archivo"]] + [x["duracion_plan"] for x in lista_resultados], 
                                        axis=1, 
                                        keys=["instancia", "60", "70", "80", "90"])

#resultados_tiempo_ejecucion.to_csv("Resultados/tiempo_ejecucion.csv")
print(resultados_tiempo_ejecucion)
axes = resultados_tiempo_ejecucion.boxplot(figsize = (5,5))
plt.ylabel("tiempo de ejecución")
plt.xlabel("calificación mínima")
plt.show()
#resultados_duracion_plan.to_csv("Resultados/duracion_plan.csv")
axes  = resultados_duracion_plan.boxplot(figsize = (5,5))
plt.ylabel("duración del plan")
plt.xlabel("calificación mínima")
plt.show()
#print(resultados_duracion_plan)