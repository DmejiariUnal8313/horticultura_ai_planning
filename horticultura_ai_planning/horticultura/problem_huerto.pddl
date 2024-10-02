(define (problem horticultura-problema-huerto)
  (:domain horticultura)
  
  (:objects
    planta3 - planta
    regadera fertilizante tijeras - herramienta
    huerto - lugar
    camino3 - camino
  )
  
  (:init
    (en-lugar planta3 huerto)
    (tiene-herramienta regadera)
    (tiene-herramienta fertilizante)
    (tiene-herramienta tijeras)
    (conectado huerto camino3)
  )
  
  (:goal
    (cosechada planta3)
  )
)