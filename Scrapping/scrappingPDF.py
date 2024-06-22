import tabula
import pandas as pd

# Path to the PDF file
# pdf_path = "./History/historico_2019008642.pdf"
# pdf_path = "./History/historico_2019006156.pdf"


def get_data_from_history_file(pdf_path: str, save_csv: bool = False) -> pd.DataFrame:
    # Extract tables from the PDF file
    tables = tabula.read_pdf(pdf_path, pages=[1,2,3,4,5], stream=True, multiple_tables=True,encoding='latin-1')
    # print(tables[1])

    filtered_table = []
    # Exibir o DataFrame final
    for data in tables:
        try:
            # Limpeza e estruturação dos dados
            # Preencher valores NaN com o valor anterior não nulo para compor disciplinas completas
            data['Unnamed: 1'] = data['Unnamed: 1'].ffill()
            data['Unnamed: 0'] = data['Unnamed: 0'].ffill()
            data['Unnamed: 2'] = data['Unnamed: 2'].ffill()
            data['Unnamed: 6'] = data['Unnamed: 6'].ffill()
            data['Nota'] = data['Nota'].ffill()
            data['Unnamed: 5'] = data['Unnamed: 5'].ffill()

            # Filtrar apenas as linhas que contêm os dados necessários
            disciplinas = data[(data['Ano/Período'].notna()) & (data['Unnamed: 1'].notna()) & (data['Nota'].notna())]

            # Selecionar e renomear as colunas desejadas
            filtro = disciplinas['Unnamed: 5'].astype(str).str.match(r"^[\d]{1}\.[\d]{1}$|^[-]*$")
            # print(filtro.sum() > filtro.shape[0] - filtro.sum(), "\n")
            if(filtro.sum() > (filtro.shape[0] - filtro.sum())):
                disciplinas = disciplinas[['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 5']]
            else:
                disciplinas = disciplinas[['Unnamed: 1', 'Unnamed: 2','Unnamed: 6']]
                
            disciplinas.columns = ['Componente Curricular', 'Docente', 'Média']
            
            condition = disciplinas['Média'].str.contains(r'^[6-9|0-1]{1,2}+\.[\d]{1}$')
            disciplinas_aprovadas = disciplinas[condition]
            filtered_table.append(disciplinas_aprovadas)
        except Exception as e:
            print("erro: ", e.args)

    result_df = pd.concat(filtered_table)
    result_df.set_index("Componente Curricular", inplace=True)
    
    if (save_csv):
        result_df.to_csv('disciplinas_concatenadas.csv', encoding='utf-8')
    return result_df
