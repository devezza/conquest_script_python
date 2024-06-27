import requests
from bs4 import BeautifulSoup
import json

def conquistas_jogos(URL, HEADERS):
    print(URL)

    response = requests.get(URL, headers=HEADERS)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, "html.parser")

    #Pegando nome do jogo

    div_game =soup.find('div', class_="profile_small_header_texture")
    if div_game:
        game_name = div_game.find('h1').text
        print('JOGO:', game_name)
    else:
        print('Nome do jogo nao encontrado')


    #Pegando conquistas
    div_achieve = soup.find('div', id='mainContents')

    if div_achieve:
        div_achieve_header = div_achieve.find('div',id="headerContent")
        qtd_achieve = div_achieve_header.find('span', class_='wt').text

        print(qtd_achieve)

        rows_achive = div_achieve.find_all('div', class_='achieveRow')

        for row in rows_achive:
            achieve_txt_holder = row.find('div', class_="achieveTxtHolder")
            if achieve_txt_holder:
                achieve_txt = achieve_txt_holder.find('div', class_="achieveTxt")
                if achieve_txt:
                    achieve_name = achieve_txt.find('h3').text
                    achieve_description = achieve_txt.find('h5').text
                    lista_conquistas.append(achieve_name)
                    print('CONQUISTA:', achieve_name)
                    print('DESCRIÇÃO:', achieve_description)
                    print('__________________________________________________')
    else:
        print('Div nao encontrada')
    return game_name, lista_conquistas

def info_jogo(URL, HEADERS):
    print(URL)

    response = requests.get(URL, headers=HEADERS)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, "html.parser")

    div_game = soup.find('div', class_="block responsive_apppage_details_left game_details underlined_links")
    if div_game:
        div_info = div_game.find('div', class_="details_block")
        if div_info:
            ano = div_info.find('b', text='Data de lançamento:').next_sibling.strip()[-4:]
            categoria_tag = div_info.find('b', text='Gênero:')
            categoria = categoria_tag.find_next_sibling('span').text.strip() if categoria_tag else None
            distribuidora_tag = div_info.find('b', text='Distribuidora:')
            distribuidora = distribuidora_tag.find_next('a').text.strip() if distribuidora_tag else None
            produtora_tag = div_info.find('b', text='Desenvolvedor:')
            produtora = produtora_tag.find_next('a').text.strip() if produtora_tag else None
    return ano, categoria, distribuidora, produtora

GAME = {
    'ano': '',
    'categoria': '',
    'conquistas': '',
    'distribuidora': '',
    'img': '',
    'nome': '',
    'produtora': ''
}

lista_conquistas = []

NUM = "1293830"
URL_JOGO = "https://store.steampowered.com/app/"+NUM
URL_CONQUISTA = "https://steamcommunity.com/stats/"+NUM+"/achievements"
HEADERS = {
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
}




game_name, lista_conquistas = conquistas_jogos(URL_CONQUISTA,HEADERS)
ano, categoria, distribuidora, produtora = info_jogo(URL_JOGO,HEADERS)

GAME['nome'] = game_name
GAME['conquistas'] = lista_conquistas
GAME['ano'] = ano
GAME['categoria'] = categoria
GAME['distribuidora'] = distribuidora
GAME['produtora'] = produtora

#EXTRAINDO JSON
json_data = json.dumps(GAME, ensure_ascii=False)
with open(game_name+'.json', 'w', encoding='utf-8') as json_file:
    json.dump(GAME, json_file, ensure_ascii=False, indent=4)

