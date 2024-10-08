"""_summary_

:return: _description_
:rtype: _type_
"""
from enum import StrEnum
from typing import Tuple, Dict, LiteralString
import pandas as pd
from src.Utils.general import get_subject_by_semester, norm_grade, DISCIPLINES
from src.Scrapping import scrappingPDF
from src.API.fetch_data import (get_combined_viewset_from_json,
                                get_competences_from_json) #, get_jwt_token


class Profile(StrEnum):
    """AI is creating summary for Profile

    :param StrEnum: [description]
    """
    HARDWARE = "HARDWARE"
    SOFTWARE = "SOFTWARE"
    IDEAL = "IDEAL"
    MEDIAN = "MEDIAN"

def get_data_from_stuprofile() -> Tuple[pd.DataFrame, Dict]:
    """_summary_

    :return: _description_
    """
    # Obter o token JWT (Quando utilizando API)
    # jwt_token = get_jwt_token()

    data = get_combined_viewset_from_json()
    # competencias = get_competences_from_json(jwt_token) # Usar quando estiver utilizando a API
    competencias = get_competences_from_json()

    # Preparar lista para o DataFrame
    rows = []

    # Iterar sobre as entradas de "blooms"
    for bloom in data["blooms"]:
        materia_id = bloom["materia"]
        docente_id = bloom["docente"]
        i_index = bloom["i_index"]
        j_index = bloom["j_index"]
        competencia = bloom["competencia"]

        # Encontrar o código da disciplina correspondente
        codigo_disciplina = None
        for materia in data["materias"]:
            if materia["id"] == materia_id:
                codigo_disciplina = materia["codigo"].split('.')[0]
                break
        # Encontrar o Nome do docente
        nome_docente = ''
        for docente in data["docentes"]:
            if docente["id"] == docente_id:
                nome_docente = docente["nome"]

        # Adicionar a linha à lista
        rows.append({
            "Codigo da Disciplina": codigo_disciplina,
            "Docente": nome_docente,
            "i_index": i_index,
            "j_index": j_index,
            "competencia": competencia
        })

    # Criar DataFrame
    df = pd.DataFrame(rows)
    df.set_index(["Codigo da Disciplina", "competencia"], inplace=True)
    df2 = df.sort_index()

    # Exibir o DataFrame
    return df2, competencias


def get_grades_by_semester(pdf_path: LiteralString) -> Dict:
    """_summary_

    :param pdf_path: _description_
    :return: _description_
    """

    history_grades = scrappingPDF.get_data_from_history_file(pdf_path, False)
    subject_by_semester = get_subject_by_semester()

    # regex = r"MSc\.|Dr[a]*\.|\(\d+h\)"
    all_semesters_data = []

    for i in range(1, 10):
        new_semester_dict = subject_by_semester[i]
        # para cada materia
        for key in new_semester_dict:
            # Recupera a nota
            if key in history_grades.index:
                # Recupera o docente
                # single_name = history_grades.loc[key]['Docente'].split(',')[0]
                # docente = re.sub(regex, "", single_name).strip()
                # new_semester_dict[key]['Docente'] = docente

                # Recupera o Nota
                nota = float(history_grades.loc[key]['Média'])
                nota = norm_grade(nota)
                new_semester_dict[key]['Nota'] = nota

                all_semesters_data.append(new_semester_dict)

    return subject_by_semester


def get_ideal_grades_by_semester(default_grade: float = 1.0) -> Dict:
    """AI is creating summary for get_ideal_grades_by_semester

    :param default_grade: [description], defaults to 1.0
    :return: [description]
    """
    # Obtém as matérias organizadas por semestre
    subject_by_semester = get_subject_by_semester()
    all_semesters_data = []

    # Itera pelos semestres (1 a 9)
    for i in range(1, 10):
        # Obtém as matérias para o semestre atual
        new_semester_dict = subject_by_semester[i]

        # Para cada matéria no semestre
        for key in new_semester_dict:

            # Define a nota ideal como 1.0
            new_semester_dict[key]['Nota'] = default_grade

            # Adiciona os dados do semestre à lista (não utilizada)
            all_semesters_data.append(new_semester_dict)

    # Retorna o dicionário de matérias por semestre com as notas e docentes atualizados
    return subject_by_semester


def get_profile_grades(profile: Profile) -> Dict:
    """_summary_

    :param profile: _description_
    :return: _description_
    """
    # Obtém as matérias organizadas por semestre
    subject_by_semester = get_subject_by_semester()
    all_semesters_data = []

    # Itera pelos semestres (1 a 9)
    for i in range(1, 10):
        # Obtém as matérias para o semestre atual
        new_semester_dict = subject_by_semester[i]

        # Para cada matéria no semestre
        for key in new_semester_dict:

            # Define a nota ideal como 1.0
            new_semester_dict[key]['Nota'] = 1.0 if key in DISCIPLINES[profile] else norm_grade(6.2)

            # Adiciona os dados do semestre à lista (não utilizada)
            all_semesters_data.append(new_semester_dict)

    # Retorna o dicionário de matérias por semestre com as notas e docentes atualizados
    return subject_by_semester