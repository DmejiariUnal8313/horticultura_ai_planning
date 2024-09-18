from django.shortcuts import render
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _parse, _ground, _search
from pyperplan.search import astar_search
from pyperplan.heuristics.blind import BlindHeuristic
import os

def generar_plan(request):
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
            estados.append(f"Antes de {action}: {estado_actual}")
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
            estados.append(f"Después de {action}: {estado_actual}")
        
        return render(request, 'plan.html', {'plan': plan_str, 'estados': estados})
    return render(request, 'index.html')