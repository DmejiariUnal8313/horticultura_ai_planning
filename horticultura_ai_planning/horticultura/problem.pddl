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