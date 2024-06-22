import pandas as pd
import numpy as np
from Utils.general import create_matrix, DISCIPLINES, salva_maior_indice
from Processing.Processing import Profile

class GrafoCompetencias:
    
    
    def __init__(self, data_base: pd.DataFrame, grades_by_semester: dict, competencia: int = None, profile: Profile = None) -> None:
        self.estrutura_info = {"acumulado": [], "disciplinas": []}
        self.maior_acumulado: int = -1
        self.maior_indice: tuple = (0,0)
        self.estrutura_notas: list[np.ndarray] = []
        
        self.data_base = data_base.copy()
        self.grades = grades_by_semester.copy()
        self.competencia = competencia
        self.profile = profile
    
    def monta_grafo_por_competencia(self, competencia: int = None) -> list:
        
        # 1 - Para cada semestre encontre as matérias que abordam essa competencia
        # 2 - A matéria consiste de um conjunto Codigo + Docente, já que o calculo deve ser feito considerando o experienciado pelo aluno
        compt = competencia if competencia else self.competencia

        for key in self.grades:
            notas_semestre = []
            acumulado_blooms = []
            for code in self.grades[key]:
                if  (not self.profile or code in DISCIPLINES[self.profile]) and (code, compt) in self.data_base.index:
                    # Chama a função que calcula a matriz integral
                    i_index = self.data_base.loc[code, compt]["i_index"]
                    j_index = self.data_base.loc[code, compt]["j_index"]
                    _, acm = create_matrix((i_index.iloc[0], j_index.iloc[0]))
                    
                    # persiste os acumulados e verifica o maior acumulado
                    acumulado_blooms.append(acm)
                    if acm > self.maior_acumulado:
                        self.maior_acumulado = acm
                        self.maior_indice = (i_index.iloc[0], j_index.iloc[0], compt)
                    
                    if not "Nota" in self.grades[key][code].keys(): self.grades[key][code]["Nota"] = 0.12
                    notas_semestre.append(self.grades[key][code]["Nota"])
                    self.estrutura_info['disciplinas'].append(self.grades[key][code]["Disciplina"])
            if len(notas_semestre):
                self.estrutura_notas.append(np.asarray(notas_semestre))
                self.estrutura_info["acumulado"].append(acumulado_blooms)
        
        if self.maior_acumulado != -1:
            salva_maior_indice(self.maior_acumulado, self.maior_indice)
        # print(self.estrutura_notas)
        # print(self.estrutura_info['acumulado'])
        # print(self.estrutura_info['disciplinas'])
                

    def calcula_valor_final(self) -> float:
        # implementa a lógica da equação matricial que gerará o resultado final
        for i in range(1, len(self.estrutura_notas)):
            s1, s2 = (self.estrutura_notas[i-1].size, self.estrutura_notas[i].size)
            qtd_pesos = s1 * s2
            tam_pesos = (s1, s2)
            pesos = np.full(tam_pesos, 1/qtd_pesos)
            
            u = self.estrutura_notas[i-1].dot(pesos)
            self.estrutura_notas[i] = self.funcao_bloom(self.estrutura_notas[i], u, self.estrutura_info["acumulado"][i])
            
        return self.calcula_indicador()
        
    def funcao_bloom(self, bias: np.ndarray, u: np.ndarray, bloom: int) -> float:
        new_array = np.ndarray(u.shape)
        for i in range(new_array.size):
            new_array[i] = (bloom[i] / self.maior_acumulado) * u[i] + bias[i]
        return new_array

    def calcula_indicador(self) -> float:
        soma_total = 0.0
        for A in self.estrutura_notas:
            soma_total += A.sum()
        
        return soma_total/len(self.estrutura_info)
    
    def gera_imagem_grafo(self) -> None:
        # idealmente consegue imprimir a estrutura do grafo.
        pass