import random as r

por_dia = 6 # quantidade de numero por dia 
qt_dias = 24 # quantidade de numero por semana

lista_numero = []


for  uma_semana in range(qt_dias):
    sorteio = 0
    while por_dia > sorteio:
        lista_numero.append(r.randint(0,9999))
        sorteio +=1
print(lista_numero)

print(lista_numero.index(1980))