# Proyecto de Planificación en IA para Horticultura

## Introducción

Este proyecto tiene como objetivo desarrollar una aplicación web para la planificación de tareas de horticultura utilizando archivos PDDL (Planning Domain Definition Language). La aplicación permite a los usuarios generar planes basados en dominios y problemas definidos en PDDL y visualizar estos planes de manera gráfica.

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas:

- `horticultura_ai_planning`
- `horticultura`
- `horticultura_page`
- `planificador`

## Descripción de las Carpetas

### `horticultura_ai_planning`

Esta carpeta contiene el entorno virtual y las dependencias necesarias para ejecutar el proyecto. Asegúrate de activar el entorno virtual antes de ejecutar cualquier comando relacionado con el proyecto.

### `horticultura`

Esta carpeta contiene el proyecto Django principal. Incluye los archivos de configuración y las aplicaciones necesarias para la funcionalidad del proyecto.

### `horticultura_page`

Esta carpeta contiene las plantillas HTML y los archivos estáticos necesarios para la interfaz de usuario de la aplicación web.

### `planificador`

Esta carpeta contiene la lógica principal de la aplicación, incluyendo las vistas, los modelos y los archivos de configuración de URL.

## Documentación del Código

### `views.py`

Este archivo contiene las vistas principales de la aplicación. Aquí se generan los planes basados en los archivos PDDL y se renderizan las páginas HTML.

```python
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
```

### `urls.py`

Este archivo contiene las rutas de URL para la aplicación.

```

from django.urls import path
from . import views

urlpatterns = [
    path('', views.generar_plan, name='generar_plan'),
]
```
### `problem.pddl`
Este archivo define el problema de horticultura en PDDL.
```
(define (problem horticultura-problema)
  (:domain horticultura)
  
  (:objects
    planta1 planta2 planta3 - planta
    regadera fertilizante tijeras - herramienta
    jardin invernadero huerto - lugar
  )
  
  (:init
    (en-lugar planta1 jardin)
    (en-lugar planta2 invernadero)
    (en-lugar planta3 huerto)
    (tiene-herramienta regadera)
    (tiene-herramienta fertilizante)
    (tiene-herramienta tijeras)
  )
  
  (:goal
    (and
      (cosechada planta1)
      (cosechada planta2)
      (cosechada planta3)
    )
  )
)
```
## Ejecución del Proyecto
Para ejecutar el proyecto, sigue estos pasos:

###  1. Activa el entorno virtual:
```
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate  # En Windows
```
### 2. Instala las dependencias
```
pip install -r requirements.txt
```
### 3. ejecuta el servidor

```
cd horticultura_ai_planning
cd horticultura
python manage.py runserver
```

### 4. Abre tu navegador y ve a http://127.0.0.1:8000/ para ver la aplicación en acción.