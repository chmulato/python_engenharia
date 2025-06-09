pressao = 250.0  # PSI (float)
temperatura = 120.0 # graus Celsius (float)
pressao_maxima = 240.0 # PSI (float)
temperatura_maxima = 110.0 # graus Celsius (float)

seguro = pressao <= pressao_maxima and temperatura <= temperatura_maxima # bool

print("Condições de operação seguras:", seguro)