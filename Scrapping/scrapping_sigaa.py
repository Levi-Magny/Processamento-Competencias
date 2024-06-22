from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.ui import WebDriverWait

service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": r"D:\Faculdade\TCC\Formulário-Pasta\Scrapping\History",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

driver = webdriver.Chrome(service=service, options=options)

#######################################################################################
############################ [requisitar e fazer o login.] ############################
#######################################################################################

# URL do formulário
url_formulario = 'https://sigaa.unifei.edu.br/sigaa/verTelaLogin.do'
driver.get(url_formulario)

# Preencher o formulário
login_input = driver.find_element(By.NAME, 'user.login')
senha_input = driver.find_element(By.NAME, 'user.senha')

login_input.send_keys('04185190212')
senha_input.send_keys('X9latvr5#kt')

# Submeter o formulário
login_input.submit()

##########################################################################################
############################ [Caso haja um formulário antes.] ############################
##########################################################################################
try:
    continue_button = driver.find_element(By.XPATH, '//input[@value="Continuar >>"]')
    print("O elemento 'Continuar >>' existe na página.")
except:
    print("O elemento 'Continuar >>' não existe na página.")


if continue_button:
    print("O elemento 'Continuar >>' existe na página.")
    continue_button.click()
    # Faça alguma ação se o elemento existir
else:
    print("O elemento 'Continuar >>' não foi encontrado na página.")


###############################################################################
############################ [Baixar o histórico.] ############################
###############################################################################

value = "menu_form_menu_discente_j_id_jsp_512348736_98_menu:A]#{ portalDiscente.historico }"

form_menu = driver.find_element(By.ID, "menu:form_menu_discente")
query = "[name='jscook_action']"
driver.execute_script(f'document.querySelector("{query}").value = "{value}";')

# print(input_hidden.get_attribute("name"))

# input_hidden.send_keys(value)
form_menu.submit()

###############################################################################
############################ [Encerrar navegador.] ############################
###############################################################################

# Fechar o navegador no final
input("Pressione Enter para encerrar o navegador...")
driver.quit()