# JOVI Smart Camera

Sistema em Python criado para tornar os recursos da câmera JOVI mais simples e intuitivos.

![Python](https://img.shields.io/badge/Python-3-blue?style=flat-square&logo=python&logoColor=white)
![FIAP](https://img.shields.io/badge/FIAP-Sprint_4-ed145b?style=flat-square)

## Sobre o projeto

O **JOVI Smart Camera** foi desenvolvido para a disciplina de **Computational Thinking with Python**, da FIAP, e evoluído na Sprint 4 com persistência de dados em arquivo e consumo de API externa.

O programa funciona no terminal e ajuda o usuário a conhecer os modos da câmera, criar configurações personalizadas e escolher um modo adequado para cada tipo de foto.

## Funcionalidades

- Visualizar os modos disponíveis na câmera;
- Cadastrar, consultar, alterar e remover perfis personalizados;
- Receber uma recomendação de modo manual, de acordo com o tipo de cena;
- Receber uma recomendação de modo automática, com base no clima real da cidade digitada (consumindo a API pública Open-Meteo);
- Simular a captura de uma foto;
- Consultar o histórico de fotos, inclusive de sessões anteriores;
- Encerrar o programa pelo menu principal.

## Conceitos de Python aplicados

- Funções com parâmetros e retornos;
- Estruturas de decisão: `if`, `elif` e `else`;
- Estruturas de repetição: `for` e `while`;
- Listas e dicionários;
- Validação de entradas e tratamento de erros com `try`/`except`;
- Persistência de dados em arquivos JSON;
- Consumo de API externa (`urllib.request`);
- Separação das responsabilidades em funções.

## Persistência de dados

Os perfis cadastrados e o histórico de fotos são salvos automaticamente em dois arquivos JSON, gerados na mesma pasta do programa:

- `perfis.json`
- `fotos.json`

Esses arquivos não vêm no repositório (são gerados na primeira execução) e são criados/atualizados sempre que um perfil ou uma foto é cadastrado, alterado ou removido. Ao reabrir o programa, os dados da última execução continuam disponíveis.

## Consumo de API

A opção **"Recomendar modo (clima real, API)"** consulta a [Open-Meteo](https://open-meteo.com/) (API pública e gratuita, sem necessidade de chave de acesso) para buscar as coordenadas da cidade digitada e o clima atual, e sugere um modo de câmera de acordo com o resultado. É necessário estar conectado à internet para usar essa opção; sem conexão, o programa mostra um aviso e volta ao menu normalmente.

## Ajustes em relação à Sprint 3

Com base no feedback recebido na Sprint 3, além da persistência e da API:

- Criada a função `mostrar_resolucoes`, eliminando a listagem de resoluções que antes era repetida em `cadastrar_perfil` e `alterar_perfil`.
- As funções de cadastro e alteração de perfil foram divididas para separar a coleta de dados do usuário (`coletar_novo_perfil`, `coletar_novo_nome`, `coletar_novo_modo`, `coletar_nova_resolucao`) da manipulação da lista de perfis (`adicionar_perfil`, `aplicar_alteracao`), que agora não fazem `input`/`print`.

## Estrutura da entrega

```text
JOVI_Sprint4/
├── main.py
├── README.md
└── documentacao_jovi_sprint4.pdf
```

## Como executar

1. Instale o Python 3 no computador.
2. Abra o terminal na pasta do projeto.
3. Execute:

```bash
python main.py
```

Não é necessário instalar bibliotecas externas — o projeto usa só a biblioteca padrão do Python (`json`, `urllib`).

## Equipe

| Nome | RM |
|---|---|
| Eduardo Felix Frois Silva | RM574103 |
| Gabriel Henrique Ongarelli Reis | RM572636 |
| Matheus de Amorim Brito | RM572435 |
| Thiago Gomes Nascimento | RM569436 |
| Vinicius Scalone Ramires | RM573783 |

## Observação

A documentação técnica completa (introdução, objetivos, descrição do projeto, organização do programa e justificativa das alterações em relação à Sprint 3) está em `documentacao_jovi_sprint4.pdf`.

Projeto desenvolvido para fins acadêmicos - **FIAP Sprint 4**.
