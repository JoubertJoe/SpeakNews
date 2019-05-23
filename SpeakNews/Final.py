from newspaper import Article
from gtts import gTTS
from pygame import mixer
import time
from bs4 import BeautifulSoup
import requests


# Inicia rotina do programa
def init():
    print("|-------------------------------")
    print("|---- S P E A K   N E W S  -----")
    print("|-------------------------------")
    print("################################")
    print("#    1 - Categorias            #")
    print("#    2 - Pesquisa Direta       #")
    print("#    3 - Notícias Hoje         #")
    print("################################")
    print("\n")
    # Pegando o Input do Usuário
    opcao = input("#    - Categoria: ")
    # chamando a opção correspondente
    if (int(opcao) > 0) & (int(opcao) < 4):  # conferindo se o input faz sentido
        # chamada do Menu.
        menu(int(opcao))
    else:
        # caso o input não faça sentido
        init()
    pass


# Menu de funções
def menu(opcaoEscolhida):
    if (opcaoEscolhida == 1):
        categoria()
    elif (opcaoEscolhida == 2):
        urlPesquisa("")
    elif (opcaoEscolhida == 3):
        print("")
    pass


# Categorias para facilitar pesquisa do usuário
def categoria():
    print("|-------------------------------------------|")
    print("|---     1 - Esporte ")
    print("|---     2 - Jogos ")
    print("|---     3 - Politica ")
    print("|---     4 - Tv ")
    print("|---     0 - Outra ")
    print("|-------------------------------------------|")
    # recebendo Categoria
    escolhido = input("|---       - Categoria: ")
    if (escolhido == 1):
        categoriaEscolhida = "Esporte"

    # Retorna a categoria escolhida
    return categoriaEscolhida


# urlPesquisa é uma função que define como será a pesquisa
# de notícias, anexando junto a URL de pesquisa os parâmetros
# necessários.
def urlPesquisa(prePesquisa):
    # Colhendo a pesquisa do Usuário
    print("|---- Digite sua pesquia: ")
    search = input("|---- ")
    # preparando a URL para fazer a pesquisa
    url = 'https://news.google.com/search?q=' + prePesquisa + search + '&hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
    # Trocar os espaços em branco por %20 (que é usado pelo google para representar o mesmo)
    url = url.replace(' ', '%20')
    # Inicia a rotina de pesquisa
    pesquisa(url)
    pass


# Efetiva a pesquisa de Notícias e armazena-as em um array
def pesquisa(url):
    html_page = requests.get(url).text
    linkArray = []  # Array onde ficarão armazenados os links
    aux = []  # Array auxiliar dos links
    soup = BeautifulSoup(html_page, "lxml")
    for link in soup.findAll('a'):
        aux.append(link.get('href'))
    # estrutura de repetição para armazenar os links (não tratados)
    for x in aux:
        if x is None:
            x = "Nada"
        else:
            if './articles' in x:
                linkArray.append(x)
                print(x)
    # Escolha do link de notícia
    # Paramêtro 0 começa do primeiro resultado
    escolhePesquisa(0, linkArray)


# Função para escolher qual notícia ler (Préviamente pesquisado)
def escolhePesquisa(nLink, link_array):
    # tratamnto de Link (Primeiro Passo)
    link_array[nLink] = link_array[nLink].replace(".", "")
    # Criando a URL da Notícia
    url = 'https://news.google.com' + link_array[nLink]
    print('|---- URL DA NOTÍCIA')
    print('|---- ' + url)
    # armazenando Notícia (artigo)
    article = Article(url)
    a = Article(url)

    # Download da Notícia, e tratamento de texto.
    a.download()
    a.parse()

    print("|---- Título da Notícia:")
    print(a.title)
    # Inicializando Sintetizador de Voz
    # Sintetizando a voz
    voz = gTTS('Fonte :' + a.title, lang='pt')
    # Salvando a voz como arquivo MP3
    voz.save('noticia.mp3')
    print('Falando...')
    # Iniciando Reprodutor de áudio
    mixer.init()
    # Carregando arquivo de voz com o título da notícia
    mixer.music.load('noticia.mp3')
    # Reproduzindo
    mixer.music.play()
    while mixer.music.get_busy():
        print('Continua falando...')
        time.sleep(1)

    # Opções de escolha da Notícia
    print("################################")
    print("#    1 - Ler Pesquisa          #")
    print("#    2 - Próxima Pesquisa      #")
    print("#    3 - Cancelar Pesquisa     #")
    print("################################")
    option = input("#      - ")

    if (option == "1"):
        # Caso escolha ouvir a notícia
        # Inicia-se a rotina de sintetização e reprodução
        voz = gTTS(a.text, lang='pt')
        voz.save('noticia.mp3')
        mixer.init()
        mixer.music.load('noticia.mp3')
        mixer.music.play()

        while mixer.music.get_busy():
            print('Continua falando...')
            time.sleep(1)

    elif (option == "2"):
        # Pula para o próximo Link da lista
        escolhePesquisa(nLink + 1)
    elif (option == "3"):
        # Recomeça o programa
        init()
    else:
        # Caso o input não seja reconhecido da forma esperada.
        print("#    -Repita por Favor")
        option = input("#      - ")


# Inicia a cadeia de execução.
init()
