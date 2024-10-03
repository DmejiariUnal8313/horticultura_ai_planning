(define (problem horticultura-problema-invernadero)
  (:domain horticultura)
  
  (:objects
    planta2 planta5 - planta
    regadera fertilizante tijeras - herramienta
    invernadero - lugar
    camino2 - camino
  )
  
  (:init
    (en-lugar planta2 invernadero)
    (en-lugar planta5 invernadero)
    (tiene-herramienta regadera)
    (tiene-herramienta fertilizante)
    (tiene-herramienta tijeras)
    (conectado invernadero camino2)
  )

(:goal
    (and
      (cosechada planta2)
      (cosechada planta5)
    )
  )
)