import sys
from src.mergesort import merge_sort
from src.quicksort import quick_sort

def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py [merge|quick] lista_de_numeros")
        print("Exemplo: python main.py merge 5 3 8 1")
        return

    algoritmo = sys.argv[1]
    lista = list(map(int, sys.argv[2:]))

    if algoritmo == "merge":
        resultado = merge_sort(lista)
    elif algoritmo == "quick":
        resultado = quick_sort(lista)
    else:
        print("Algoritmo inválido! Use 'merge' ou 'quick'")
        return

    print("Entrada:", lista)
    print("Saída:", resultado)


if __name__ == "__main__":
    main()
