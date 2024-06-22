import numpy as np
import pandas as pd
from difflib import SequenceMatcher

MAIOR_INDICE = (3, 2)

def create_matrix(index: tuple) -> tuple[np.ndarray, int]:
    A = np.zeros(shape=(4,6))
    B = np.zeros(shape=(index[0]+1,index[1]+1))
    for i in range(4):
        for j in range(6):
            A[i][j] = i + j + 1

    for i in range(index[0]+1):
        for j in range(index[1]+1):
            B[i][j] = int(A[:i+1, :j+1].sum())
    
    return B, int(B[index[0]][index[1]])

def salva_maior_indice(acumulado: int, posicao: tuple[int, int, int]) -> None:
    with open('Data/maiores_blooms.csv', 'a') as f:
        linha = f"{posicao[2]},{acumulado},{posicao[0]},{posicao[1]}\n"
        f.write(linha)

def norm_grade(grade: float) -> float:
    """_summary_

    Args:
        grade (float): _description_

    Returns:
        float: _description_
    """
    grade_array = np.random.uniform(6.0, 10.0, 30)
    grade_array = np.append(grade_array, grade)
    valor_nota = (grade - grade_array.min())/(grade_array.max() - grade_array.min())
    return valor_nota
    
    # std = np.std(grade_array, ddof=1)
    # mean = np.mean(grade_array)
    
    # z = (grade - mean)/std
    # z_min = (grade_array.min() - mean)/std
    # z_max = (grade_array.max() - mean)/std
    
    # valor_nota = (z - z_min)/(z_max - z_min)


def load_excel_as_dict(file_path):
    # Carregar todas as planilhas do arquivo Excel
    all_sheets_df = pd.read_excel(file_path, sheet_name=None)

    # Criar um dicionário para armazenar os dados das planilhas, exceto a última
    sheets_dict = {}
    for sheet_name, df in list(all_sheets_df.items())[:-1]:
        # Transformar a planilha em um dicionário com a primeira coluna como chave
        sheet_dict = {}
        for index, row in df.iterrows():
            # Usar a primeira coluna como chave
            key = row.iloc[0]
            # Excluir a primeira coluna dos valores
            value = row.iloc[1:].to_dict()
            sheet_dict[key] = value
        sheets_dict[int(sheet_name)] = sheet_dict

    return sheets_dict


def get_subject_by_semester(semester: int = None) -> dict:
    """
    # Recupera as matérias por semestre
    
    Essa função separa as matérias de cada semestre indexadas pelos seus respectivos códigos

    ## Parameters:
        - `semester (int, optional)`: Um semestre específico [1 a 9]. Defaults to None.

    ## Returns:
        - `dict`: Um dicionário indexado por um inteiro [1 a 9], cujos valores são dicionários indexados por códigos de matérias [ex: ECOI02]
    """
    # Exemplo de uso
    file_path = r'D:\Faculdade\TCC\Formulário-Pasta\Scrapping\Utils\Mapeamento-Disciplinas.xlsx'
    sheets_dict = load_excel_as_dict(file_path)
    if semester:
        return sheets_dict[semester]
    else:
        return sheets_dict


def same_name(a: str, b: str) -> bool:
    return SequenceMatcher(None, a, b).ratio() > 0.88

import numpy as np

def similaridade_por_cosseno(lista1:list, lista2:list):
    # Calcular o produto escalar entre os dois vetores
    vetor2 = np.array(lista1)
    vetor1 = np.array(lista2)
    produto_escalar = np.dot(vetor1, vetor2)
    
    # Calcular a norma (magnitude) de cada vetor
    norma_vetor1 = np.linalg.norm(vetor1)
    norma_vetor2 = np.linalg.norm(vetor2)
    
    # Calcular a similaridade por cosseno
    similaridade = produto_escalar / (norma_vetor1 * norma_vetor2)
    
    return similaridade

def distancia_euclidiana(lista1, lista2):
    # Converter as listas em arrays do NumPy
    vetor1 = np.array(lista1)
    vetor2 = np.array(lista2)
    
    # Calcular a diferença entre os vetores
    diferenca = vetor1 - vetor2
    
    # Calcular a distância euclidiana
    distancia = np.sqrt(np.sum(diferenca ** 2))
    
    return distancia

DISCIPLINES = {
  "HARDWARE": np.array([
    "EELI02",
    "EELI03",
    "ECOI12",
    "EELI07",
    "ECAI26",
    "EELI10",
    "EELI11",
    "ECOI10",
    "EELI12",
    "EELI13",
    "EELI14",
    "EELI15",
    "ECAI04",
    "ECOI21",
    "ECAI11",
    "ECAI44",
    "ECOI18",
    "ECOI33",
    "ECAI05",
    "ECAI07",
    "ECOI33",
    "ECAI13",
    "ECOI07",
    "ECOI32",
    "ECOI19",
  ]),
  "SOFTWARE": np.array([
    "ECOI02",
    "ECOI03",
    "ECOI04",
    "ECOI08",
    "ECOI14",
    "ECOI30",
    "ECOI15",
    "ECOI16",
    "ECOI11",
    "ECOI13",
    "ECOI22",
    "ECOI25",
    "ECOI09",
    "ECOI23",
    "ECOI24",
    "ECOI26",
  ]),
  "UNCLASSIFIED": np.array([
    'EAMI30',
    'ECAI29',
    'ECO038',
    'ECOI01',
    'ECOI20',
    'ECOI61',
    'EMBI02',
    'EMEI02',
    'EMEI06',
    'EMEI07',
    'EMEI08',
    'EMTI02',
    'EMTI03',
    'EPRI02',
    'EPRI04',
    'EPRI30',
    'FISI01',
    'FISI02',
    'FISI03',
    'FISI04',
    'FISI04',
    'FISI05',
    'FISI06',
    'FISI07',
    'HUMI01',
    'HUMI02',
    'HUMI04',
    'HUMI06',
    'MATI01',
    'MATI02',
    'MATI03',
    'MATI03',
    'MATI04',
    'MATI05',
    'MATI06',
    'MATI07',
    'MATI08'])
}