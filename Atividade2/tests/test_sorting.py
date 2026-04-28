from src.mergesort import merge_sort
from src.quicksort import quick_sort

def test_merge_sort():
    assert merge_sort([3, 1, 2]) == [1, 2, 3]
    assert merge_sort([]) == []
    assert merge_sort([5]) == [5]

def test_quick_sort():
    assert quick_sort([3, 1, 2]) == [1, 2, 3]
    assert quick_sort([]) == []
    assert quick_sort([5]) == [5]

if __name__ == "__main__":
    test_merge_sort()
    test_quick_sort()
    print("Todos os testes passaram!")
