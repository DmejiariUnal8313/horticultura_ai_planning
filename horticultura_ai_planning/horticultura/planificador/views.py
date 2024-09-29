from django.shortcuts import render
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _parse, _ground, _search
from pyperplan.search import astar_search
from pyperplan.heuristics.blind import BlindHeuristic
import os
import matplotlib
matplotlib.use('Agg')  # Usar el backend 'Agg' para evitar problemas de GUI
import matplotlib.pyplot as plt
import pandas as pd

def generar_plan(request):
    """
    Genera un plan basado en los archivos PDDL y lo muestra en una página web.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el plan generado y la simulación de resultados.
    """

    if request.method == 'POST':
        # Obtener la ruta absoluta del directorio actual
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        domain_file = os.path.join(base_dir, 'domain.pddl')
        problem_file = os.path.join(base_dir, 'problem.pddl')
        
        parser = Parser(domain_file, problem_file)
        domain = parser.parse_domain()
        problem = parser.parse_problem(domain)
        
        task = _ground(problem)
        heuristic = BlindHeuristic(task)
        plan = _search(task, astar_search, heuristic)
        
        plan_str = '\n'.join(str(action) for action in plan)
        
        # Simulación de resultados
        estados = []
        estado_actual = {}
        for action in plan:
            estados.append(f"Antes de {action}: {estado_actual.copy()}")
            # Actualizar estado_actual según la acción
            if "plantar" in str(action):
                planta = str(action).split()[1]
                estado_actual[planta] = "plantada"
            elif "regar" in str(action):
                planta = str(action).split()[1]
                estado_actual[planta] = "regada"
            elif "fertilizar" in str(action):
                planta = str(action).split()[1]
                estado_actual[planta] = "fertilizada"
            elif "podar" in str(action):
                planta = str(action).split()[1]
                estado_actual[planta] = "podada"
            elif "cosechar" in str(action):
                planta = str(action).split()[1]
                estado_actual[planta] = "cosechada"
            estados.append(f"Después de {action}: {estado_actual.copy()}")
        
        # Generar gráfico
        generar_grafico(plan, base_dir)
        
        # Convertir estados a DataFrame para mostrar en tabla
        df_estados = pd.DataFrame(estados, columns=['Estado'])
        
        return render(request, 'plan.html', {'plan': plan_str, 'estados': estados, 'df_estados': df_estados.to_html(classes='table table-striped')})
    return render(request, 'index.html')

def generar_grafico(plan, base_dir):
    """
    Genera un gráfico del plan y lo guarda como una imagen.

    Args:
        plan (list): La lista de acciones del plan.
        base_dir (str): El directorio base donde se guardará la imagen.
    """


    fig, ax = plt.subplots()
    y = range(len(plan))
    x = [str(action) for action in plan]
    
    ax.barh(y, [1] * len(plan), align='center')
    ax.set_yticks(y)
    ax.set_yticklabels(x)
    ax.invert_yaxis()  # Invertir el eje y para que el primer paso esté en la parte superior
    ax.set_xlabel('Acciones')
    ax.set_title('Plan de Horticultura')
    
    # Guardar el gráfico como una imagen
    grafico_path = os.path.join(base_dir, 'static', 'plan_grafico.png')
    plt.savefig(grafico_path)
    plt.close(fig)