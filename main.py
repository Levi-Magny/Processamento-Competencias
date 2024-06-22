import os
from Processing.Processing import *
from Processing.GrafoCompetencias import GrafoCompetencias
from Processing.Plot import spider_plot, bar_plot

current_path = os.path.dirname(__file__)

def get_profile_vector(competencias: list, data_base, grades_by_semester, profile: Profile = None) -> tuple[list, list]:
    columns = []
    results = []
    for compt in competencias:
        grafo = GrafoCompetencias(data_base, grades_by_semester, compt['id'], profile)
        grafo.monta_grafo_por_competencia()
        result = grafo.calcula_valor_final()
        
        columns.append(compt['descricao'])
        results.append(result)
    
    return columns, results

def filter_valid_competences(param_vector, student, columns) -> tuple[list, list, list]:
    new_param_vector = []
    new_student = []
    new_columns = []
    for i in range(len(param_vector)):
        if param_vector[i] != 0:
            new_param_vector.append(param_vector[i])
            new_student.append(student[i])
            new_columns.append(columns[i])
    return new_param_vector, new_student, new_columns

def process_columns_and_params_vectors(data_base: pd.DataFrame, competencias: dict, profile: Profile):
    # Pega os vetores do aluno real,
    if profile == Profile.SOFTWARE:
        software_grades = get_profile_grades(Profile.SOFTWARE)
        _, param_results = get_profile_vector(competencias, data_base, software_grades, profile=Profile.SOFTWARE)
    elif profile == Profile.HARDWARE:
        hardware_grades = get_profile_grades(Profile.HARDWARE)
        _, param_results = get_profile_vector(competencias, data_base, hardware_grades, profile=Profile.HARDWARE)
    elif profile == Profile.IDEAL:
        print("Criando Aluno Ideal...")
        ideal_grades = get_ideal_grades_by_semester()
        _, param_results = get_profile_vector(competencias, data_base, ideal_grades)
    
    print("Criando Aluno Médio...")
    median_grades = get_ideal_grades_by_semester(norm_grade(6.2))
    cols, median_results = get_profile_vector(competencias, data_base, median_grades)
    
    return cols, median_results, param_results

def create_profile_vectors(pdf_path: str, data_base: pd.DataFrame, competencias: dict, profile: Profile):

    grades_by_semester = get_grades_by_semester(pdf_path)
    _, results = get_profile_vector(competencias, data_base, grades_by_semester, profile=profile if profile != Profile.IDEAL else None)

    cols, median_results, param_results = process_columns_and_params_vectors(data_base, competencias, profile)
    
    # Normaliza as Notas
    maior = max(param_results)
    norm_results = [x/maior for x in results]
    norm_param_results = [x/maior for x in param_results]
    norm_median_results = [x/maior for x in median_results]
    
    # Calcula a similaridade com o original
    median_euclidean = distancia_euclidiana(norm_median_results, norm_param_results)
    student_euclidean = distancia_euclidiana(norm_results, norm_param_results)
    norm_similarity = 1 - student_euclidean/median_euclidean

    param, student, cols = filter_valid_competences(norm_param_results, norm_results, cols)

    return norm_similarity, param, student, cols


if __name__ == "__main__":

    pefil = Profile.HARDWARE
    
    # Path to the PDF file
    pdf_path = [fr"{current_path}\History\historico_2019008642.pdf",
                fr"{current_path}\History\historico_2019006156.pdf",
                fr"{current_path}\History\historico_2019002925.pdf"]

    similarity_list = []
    student_list = []
    compt_cols = []
    param_list = []
    alunos_nome = []

    aluno_numero = 1

    print("Recuperando dados via API...")
    data_base, competencias = get_data_from_stuprofile()
    
    for path in pdf_path:

        similarity, param, student, cols = create_profile_vectors(path, data_base, competencias, pefil)
        similarity_list.append(similarity)
        student_list.append(student)
        alunos_nome.append(f"Auno {aluno_numero}")
        
        aluno_numero += 1
        
        if not len(compt_cols):
            param_list = param
            compt_cols = cols

        print(f"Similaridade Aluno 1: {similarity}")

    spider_plot(compt_cols, [*alunos_nome, f"Aluno {pefil}"], [*student_list, param_list], file_name="Img/Alunos_Ideal.html")
    bar_plot(compt_cols, [*alunos_nome, f"Aluno {pefil}"], [*student_list, param_list], file_name="Img/bar_Alunos_Ideal.html")
