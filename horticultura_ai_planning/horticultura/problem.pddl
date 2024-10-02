(define (problem horticultura-problema)
  (:domain horticultura)
  
  (:objects
    planta1 planta2 planta3 planta4 planta5 - planta
    regadera fertilizante tijeras - herramienta
    jardin invernadero huerto - lugar
    camino1 camino2 camino3 - camino
  )
  
  (:init
    (en-lugar planta1 jardin)
    (en-lugar planta2 invernadero)
    (en-lugar planta3 huerto)
    (en-lugar planta4 jardin)
    (en-lugar planta5 invernadero)
    (tiene-herramienta regadera)
    (tiene-herramienta fertilizante)
    (tiene-herramienta tijeras)
    (conectado jardin camino1)
    (conectado camino1 invernadero)
    (conectado invernadero camino2)
    (conectado camino2 huerto)
    (conectado huerto camino3)
    (conectado camino3 jardin)
    (en-camino camino1 jardin)
    (en-camino camino1 invernadero)
    (en-camino camino2 invernadero)
    (en-camino camino2 huerto)
    (en-camino camino3 huerto)
    (en-camino camino3 jardin)
  )
  
  (:goal
    (and
      (cosechada planta1)
      (cosechada planta2)
      (cosechada planta3)
      (cosechada planta4)
      (cosechada planta5)
    )
  )
)