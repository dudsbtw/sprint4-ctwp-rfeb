# projeto da sprint 4 de computational thinking with python
# sistema para facilitar o uso dos recursos da camera JOVI
# equipe: Eduardo Frois, Gabriel Reis, Matheus Brito,
# Thiago Nascimento e Vinicius Ramires

import json
import urllib.request
import urllib.parse
import urllib.error

MODOS = [
    {"nome": "Retrato", "descricao": "Destaca pessoas e desfoca o fundo", "cena": "Uma pessoa"},
    {"nome": "Noturno", "descricao": "Melhora fotos em lugares escuros", "cena": "Um lugar escuro"},
    {"nome": "Paisagem", "descricao": "Realca cores de ambientes abertos", "cena": "Uma paisagem"},
    {"nome": "Movimento", "descricao": "Ajuda a evitar fotos borradas", "cena": "Algo em movimento"}
]
RESOLUCOES = ["12 MP", "50 MP", "108 MP"]
ARQUIVO_PERFIS = "perfis.json"
ARQUIVO_FOTOS = "fotos.json"

# le os perfis salvos, ou comeca uma lista vazia se o arquivo nao existe
def carregar_perfis():
    try:
        with open(ARQUIVO_PERFIS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# grava a lista de perfis no arquivo json
def salvar_perfis(perfis):
    with open(ARQUIVO_PERFIS, "w", encoding="utf-8") as arquivo:
        json.dump(perfis, arquivo, ensure_ascii=False, indent=2)

# le o historico de fotos salvo, ou comeca uma lista vazia se o arquivo nao existe
def carregar_fotos():
    try:
        with open(ARQUIVO_FOTOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# grava o historico de fotos no arquivo json
def salvar_fotos(fotos):
    with open(ARQUIVO_FOTOS, "w", encoding="utf-8") as arquivo:
        json.dump(fotos, arquivo, ensure_ascii=False, indent=2)

# valida numeros inteiros e o intervalo permitido
def ler_numero(mensagem, menor, maior):
    while True:
        try:
            numero = int(input(mensagem))
            if menor <= numero <= maior:
                return numero
            print("Digite um numero entre", menor, "e", maior)
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")

# aceita somente respostas S ou N
def ler_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta == "s":
            return True
        if resposta == "n":
            return False
        print("Digite S para sim ou N para nao.")

# mostra os modos disponiveis
def mostrar_modos(modos):
    print("\n--- MODOS DA CAMERA ---")
    for numero, modo in enumerate(modos, 1):
        print(f"{numero} - {modo['nome']}: {modo['descricao']}")

# mostra as resolucoes disponiveis
def mostrar_resolucoes(resolucoes):
    print("\n--- RESOLUCOES ---")
    for numero, resolucao in enumerate(resolucoes, 1):
        print(numero, "-", resolucao)

# mostra os perfis cadastrados
def listar_perfis(perfis):
    print("\n--- PERFIS CADASTRADOS ---")
    if not perfis:
        print("Nenhum perfil cadastrado.")
        return False
    for numero, perfil in enumerate(perfis, 1):
        flash = "ativado" if perfil["flash"] else "desativado"
        grade = "ativada" if perfil["grade"] else "desativada"
        print(f"\n{numero} - {perfil['nome']}\nModo: {perfil['modo']}"
              f"\nResolucao: {perfil['resolucao']}\nFlash: {flash}\nGrade: {grade}")
    return True

# retorna o perfil escolhido ou None quando a lista esta vazia
def escolher_perfil(perfis, mensagem):
    if not listar_perfis(perfis):
        return None
    numero = ler_numero(mensagem, 1, len(perfis))
    return perfis[numero - 1]

# verifica se ja existe um perfil com esse nome (dado puro, sem entrada/saida)
def nome_em_uso(perfis, nome, ignorar=None):
    return any(perfil is not ignorar and perfil["nome"].lower() == nome.lower() for perfil in perfis)

# coleta os dados de um novo perfil com o usuario, sem mexer na lista de perfis
def coletar_novo_perfil(perfis, modos, resolucoes):
    print("\n--- CADASTRAR PERFIL ---")
    nome = input("Nome do perfil: ").strip()
    if not nome:
        print("O nome nao pode ficar vazio.")
        return None
    if nome_em_uso(perfis, nome):
        print("Ja existe um perfil com esse nome.")
        return None
    mostrar_modos(modos)
    modo = modos[ler_numero("Escolha o modo: ", 1, len(modos)) - 1]["nome"]
    mostrar_resolucoes(resolucoes)
    resolucao = resolucoes[ler_numero("Escolha a resolucao: ", 1, len(resolucoes)) - 1]
    flash = ler_sim_nao("Ativar flash automatico? (S/N): ")
    grade = ler_sim_nao("Ativar grade? (S/N): ")
    return {"nome": nome, "modo": modo, "resolucao": resolucao, "flash": flash, "grade": grade}

# adiciona o perfil na lista e salva (so manipulacao de dados, sem input/print)
def adicionar_perfil(perfis, perfil):
    perfis.append(perfil)
    salvar_perfis(perfis)

# junta a coleta e a adicao do novo perfil
def cadastrar_perfil(perfis, modos, resolucoes):
    perfil = coletar_novo_perfil(perfis, modos, resolucoes)
    if perfil is None:
        return
    adicionar_perfil(perfis, perfil)
    print("Perfil cadastrado com sucesso!")

# pergunta qual campo do perfil o usuario quer alterar
def escolher_campo_para_alterar():
    print("\n1 - Nome\n2 - Modo\n3 - Resolucao\n4 - Flash\n5 - Grade\n6 - Cancelar")
    return ler_numero("Opcao: ", 1, 6)

# coleta o novo nome, validando vazio e duplicidade (ignorando o proprio perfil)
def coletar_novo_nome(perfis, perfil):
    novo_nome = input("Novo nome: ").strip()
    if not novo_nome or nome_em_uso(perfis, novo_nome, ignorar=perfil):
        print("Nome vazio ou ja cadastrado.")
        return None
    return novo_nome

# coleta o novo modo escolhido pelo usuario
def coletar_novo_modo(modos):
    mostrar_modos(modos)
    return modos[ler_numero("Novo modo: ", 1, len(modos)) - 1]["nome"]

# coleta a nova resolucao escolhida pelo usuario
def coletar_nova_resolucao(resolucoes):
    mostrar_resolucoes(resolucoes)
    return resolucoes[ler_numero("Nova resolucao: ", 1, len(resolucoes)) - 1]

# aplica um novo valor num campo do perfil (so manipulacao de dados, sem input/print)
def aplicar_alteracao(perfil, campo, valor):
    perfil[campo] = valor

# junta a escolha do campo, a coleta do novo valor e a aplicacao da alteracao
def alterar_perfil(perfis, modos, resolucoes):
    perfil = escolher_perfil(perfis, "\nEscolha o perfil: ")
    if perfil is None:
        return
    opcao = escolher_campo_para_alterar()
    if opcao == 1:
        novo_nome = coletar_novo_nome(perfis, perfil)
        if novo_nome is None:
            return
        aplicar_alteracao(perfil, "nome", novo_nome)
    elif opcao == 2:
        aplicar_alteracao(perfil, "modo", coletar_novo_modo(modos))
    elif opcao == 3:
        aplicar_alteracao(perfil, "resolucao", coletar_nova_resolucao(resolucoes))
    elif opcao == 4:
        aplicar_alteracao(perfil, "flash", not perfil["flash"])
    elif opcao == 5:
        aplicar_alteracao(perfil, "grade", not perfil["grade"])
    else:
        print("Alteracao cancelada.")
        return
    salvar_perfis(perfis)
    print("Perfil alterado com sucesso!")

# remove um perfil depois da confirmacao e salva no arquivo
def remover_perfil(perfis):
    perfil = escolher_perfil(perfis, "\nEscolha o perfil: ")
    if perfil is None:
        return
    if ler_sim_nao("Confirma a remocao? (S/N): "):
        perfis.remove(perfil)
        salvar_perfis(perfis)
        print("Perfil removido com sucesso!")
    else:
        print("Remocao cancelada.")

# controla as funcoes relacionadas aos perfis
def menu_perfis(perfis, modos, resolucoes):
    while True:
        print("\n--- MENU DE PERFIS ---\n1 - Cadastrar\n2 - Ver\n3 - Alterar\n4 - Remover\n5 - Voltar")
        opcao = ler_numero("Opcao: ", 1, 5)
        if opcao == 1:
            cadastrar_perfil(perfis, modos, resolucoes)
        elif opcao == 2:
            listar_perfis(perfis)
        elif opcao == 3:
            alterar_perfil(perfis, modos, resolucoes)
        elif opcao == 4:
            remover_perfil(perfis)
        else:
            return
        input("\nPressione ENTER para voltar ao menu...")

# recomenda um modo conforme o tipo de cena escolhida manualmente
def recomendar_modo(modos):
    print("\n--- ASSISTENTE DE CENA ---")
    for numero, modo in enumerate(modos, 1):
        print(numero, "-", modo["cena"])
    modo = modos[ler_numero("Opcao: ", 1, len(modos)) - 1]
    print("\nModo recomendado:", modo["nome"])
    print(modo["descricao"])

# busca a latitude e longitude de uma cidade na api de geocodificacao
def buscar_coordenadas(cidade):
    parametros = urllib.parse.urlencode({"name": cidade, "count": 1, "language": "pt"})
    url = "https://geocoding-api.open-meteo.com/v1/search?" + parametros
    with urllib.request.urlopen(url, timeout=6) as resposta:
        dados = json.loads(resposta.read())
    resultados = dados.get("results")
    if not resultados:
        return None
    local = resultados[0]
    return local["latitude"], local["longitude"], local["name"]

# busca o clima atual na api open-meteo a partir das coordenadas
def buscar_clima(latitude, longitude):
    parametros = urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,cloud_cover,precipitation,is_day"
    })
    url = "https://api.open-meteo.com/v1/forecast?" + parametros
    with urllib.request.urlopen(url, timeout=6) as resposta:
        dados = json.loads(resposta.read())
    return dados["current"]

# decide o modo mais adequado de acordo com os dados do clima
def escolher_modo_pelo_clima(clima):
    if clima["is_day"] == 0 or clima["cloud_cover"] > 80:
        return "Noturno"
    if clima["precipitation"] > 0:
        return "Movimento"
    if clima["cloud_cover"] < 30:
        return "Paisagem"
    return "Retrato"

# recomenda um modo com base no clima real da cidade, consumindo a api open-meteo
def recomendar_modo_clima():
    print("\n--- ASSISTENTE DE CENA (CLIMA REAL) ---")
    cidade = input("Digite sua cidade: ").strip()
    if not cidade:
        print("A cidade nao pode ficar vazia.")
        return
    try:
        local = buscar_coordenadas(cidade)
        if local is None:
            print("Cidade nao encontrada.")
            return
        latitude, longitude, nome = local
        clima = buscar_clima(latitude, longitude)
        print(f"\nClima atual em {nome}:")
        print(f"Temperatura: {clima['temperature_2m']} C")
        print(f"Nuvens: {clima['cloud_cover']}%")
        print(f"Chuva: {clima['precipitation']} mm")
        modo = escolher_modo_pelo_clima(clima)
        print("\nModo recomendado:", modo)
    except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError):
        print("Nao foi possivel consultar o clima agora. Verifique sua internet e tente novamente.")

# simula uma foto, adiciona ao historico e salva no arquivo
def capturar_foto(perfis, fotos):
    perfil = escolher_perfil(perfis, "\nEscolha o perfil: ")
    if perfil is None:
        print("Cadastre um perfil antes de tirar uma foto.")
        return
    fotos.append({"numero": len(fotos) + 1, "perfil": perfil["nome"],
                  "modo": perfil["modo"], "resolucao": perfil["resolucao"]})
    salvar_fotos(fotos)
    print("Foto", len(fotos), "capturada com sucesso!")

# mostra as fotos registradas, incluindo as de sessoes anteriores
def mostrar_historico(fotos):
    print("\n--- HISTORICO DE FOTOS ---")
    if not fotos:
        print("Nenhuma foto foi tirada.")
        return
    for foto in fotos:
        print(f"Foto {foto['numero']} - Perfil: {foto['perfil']} - "
              f"Modo: {foto['modo']} - {foto['resolucao']}")
    print("Total de fotos:", len(fotos))

# exibe o menu principal ate o usuario escolher sair
def menu_principal():
    perfis = carregar_perfis()
    fotos = carregar_fotos()
    while True:
        print("\n=== JOVI SMART CAMERA ===\n1 - Ver modos\n2 - Gerenciar perfis"
              "\n3 - Recomendar modo (cena)\n4 - Recomendar modo (clima real, API)"
              "\n5 - Simular foto\n6 - Ver historico\n7 - Sair")
        opcao = ler_numero("Opcao: ", 1, 7)
        if opcao == 1:
            mostrar_modos(MODOS)
        elif opcao == 2:
            menu_perfis(perfis, MODOS, RESOLUCOES)
            continue
        elif opcao == 3:
            recomendar_modo(MODOS)
        elif opcao == 4:
            recomendar_modo_clima()
        elif opcao == 5:
            capturar_foto(perfis, fotos)
        elif opcao == 6:
            mostrar_historico(fotos)
        else:
            print("Programa finalizado.")
            return
        input("\nPressione ENTER para voltar ao menu...")

# inicia o programa somente quando este arquivo for executado
if __name__ == "__main__":
    menu_principal()
