import numpy as np
from src.Utils.general import create_matrix, norm_grade


def test_create_matrix():
    # Teste para verificar a matriz e o valor acumulado
    index = (2, 3)
    B, acumulado = create_matrix(index)

    # Verifica se o shape da matriz está correto
    assert B.shape == (index[0]+1, index[1]+1)

    # Verifica se o valor acumulado está correto
    valor_esperado = int(B[index[0], index[1]])
    assert acumulado == valor_esperado

    # Teste adicional para valores específicos
    assert B[2, 3] == 42.0


def test_norm_grade():
    # Teste para verificar se o valor normalizado está entre 0 e 1
    grade = 8.0
    valor_normalizado = norm_grade(grade)

    # Verifica se o valor está entre 0 e 1
    assert 0.0 <= valor_normalizado <= 1.0

    # Teste com diferentes valores de nota
    grade_menor = 6.0
    grade_maior = 10.0
    assert norm_grade(grade_menor) < norm_grade(grade_maior)
