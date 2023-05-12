def CrearPlan(instancia):
    tiempo = 0
    plan = [] # Plan a retornar
    
    # Primero escoge las actividad obligatorias
    for actividad in instancia:
        if actividad.es_obligatoria:
            # ResolverDependencias(instancia, actividad) retorna un plan
            # que resuelve todas las dependencias de la actividad dada y las
            # dependencias de las dependencias recursivamente.
            # Logra esto siguiendo un algoritmo de búsqueda post-orden en arbol
            # Si una actividad ya está en el plan, no la agrega
            plan_con_dependencias = ResolverDependencias(actividad, plan)
            plan = plan + plan_con_dependencias

    # Ahora que el plan tiene todas las actividades obligatorias
    # las elimina de la instancia como si no hubieran existido
    # Además, deduce el valor de la actividad del valor objetivo
    # del subtema al que pertenece
    for actividad in plan:
        # Actualiza datos del subtema
        actividad.subtema.calif_min -= actividad.valor
        # Actualiza datos del plan
        tiempo += actividad.tiempo
        # Elimina todas las referencias a la actividad 
        # en la instancia
        # incluyendo las referencias que la 
        # toman como dependencia de otra actividad
        instancia.actividades.pop(actividad)
    
    # Ahora, por cada subtema tenemos una calificación 
    # mínima y una lista de actividades, debemos de escoger
    # las actividades de este subtema tal que la suma de estos 
    # valores llegue a kmin pero tambien 
    # minimizando el tiempo que toman las actividades 
    posibles_soluciones_subtemas = dict()

    # Por cada actividad, agrego una lista de soluciones voraces al problema
    # sin tomar en cuenta dependencias
    for actividad in plan:
        lista_soluciones = []
        
        # el algoritmo voraz_tiempo retorna la lista de actividades
        # generada al agregar las actividades que tomen menos tiempo
        # hasta que se alcance la calificación mínima de la actividad
        lista_soluciones[0] = voraz_tiempo(actividad)
        
        # el algoritmo voraz_valor hace lo mismo pero agrega
        # empezando con las actividades con mayor valor
        lista_soluciones[1] = (voraz_valor(actividad))
        
        # el algoritmo voraz_densidad hace lo mismo pero agrega
        # empezando con las actividades con mayor valor por tiempo
        lista_soluciones[2] = (voraz_densidad(actividad))
        
        # Guarda estas posibles elecciones de actividades
        # por subtema ahora tengo 3 posibles elecciones de actividades
        # que satisfacen la calificación mínima
        posibles_soluciones_subtemas[actividad] = lista_soluciones

    mejor_tiempo = +infinito
    mejor_resto_plan = []
    
    # ahora intenta todas las formas de escoger una 
    # solucion por cada subtema. Como generamos 3 posibles 
    # soluciones por subtema, en total hay 3 ** cantidad_de_subtemas
    # formas de hacerlo, ya que como máximo hay 8 subtemas, 
    # máximo hay alrededor de 6000 formas de hacerlo
    for combinacion_soluciones in producto_cartesiano(posibles_soluciones_subtemas):
        # Ya que las soluciones voraces se generaron 
        # sin tomar en cuenta dependencias, se resuelven aquí 
        # (En retrospectiva esto se pudo haber hecho desde la generación
        # de soluciones por actividad para ahorrar mucho tiempo)
        resto_del_plan = []
        for actividad in combinacion_soluciones:
            resto_del_plan += ResolverDependencias(actividad, resto_del_plan)
        # Si el nuevo plan generado es mejor que el 
        # anteriormente mejor (ocupa menos tiempo)
        # escoge el nuevo plan como el nuevo mejor
        if tiempo(resto_plan) < mejor_tiempo:
            mejor_resto_plan = resto_plan
            mejor_tiempo = tiempo(resto_plan)
    
    # Agrega el mejor resto del plan al plan final
    plan += mejor_resto_plan
    tiempo += mejor_tiempo
    # retorna el plan generado con el tiempo que toma
    return (plan, tiempo)