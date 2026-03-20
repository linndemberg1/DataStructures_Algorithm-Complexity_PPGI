from selection_sort import selection_sort

def testar(lista):
    resultado = selection_sort(lista.copy())
    esperado = sorted(lista)

    if resultado == esperado:
        print(f"OK  -> {lista} => {resultado}")
    else:
        print(f"ERRO -> {lista} => {resultado} (esperado {esperado})")


entrada = input("Digite os números separados por '-': ")
lista = [int(x.strip()) for x in entrada.split("-")]

testar(lista)
