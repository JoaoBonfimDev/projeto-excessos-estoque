# Projeto Excessos do Estoque

Aplicação web desenvolvida em Python e Flask para praticar conceitos de desenvolvimento front-end, back-end, banco de dados e tratamento de dados através de um sistema de controle de estoque.

## Sobre o projeto

A ideia deste projeto surgiu a partir da observação de uma necessidade real no ambiente de varejo: facilitar o controle de produtos excedentes do estoque e a consulta de suas respectivas quantidades.

O sistema permite registrar entradas e saídas de produtos, considerando modelo, tamanho e quantidade disponível.

Além das movimentações manuais, o projeto passou a trabalhar com uma base de estoque proveniente de planilha, utilizando Python e Pandas para leitura, tratamento, validação e preparação dos dados antes de sua integração com o banco de dados.

O projeto está em desenvolvimento e faz parte do meu processo de aprendizado em programação, análise de dados e desenvolvimento de aplicações web.

## Funcionalidades atuais

- Registro de entradas e saídas de produtos
- Controle por modelo, tamanho e quantidade
- Validação de estoque insuficiente
- Persistência de dados utilizando SQLite
- Comunicação entre formulário HTML e back-end Flask
- Interface responsiva para computadores e celulares
- Estrutura inicial para consulta de estoque
- Leitura de planilhas `.xlsb` utilizando Pandas
- Tratamento e limpeza dos dados importados
- Separação automática de modelo e tamanho a partir da descrição do produto
- Conversão e validação dos tipos de dados
- Consolidação de produtos equivalentes por modelo e tamanho
- Preparação dos dados para sincronização com o banco de dados

## Tratamento dos dados

O projeto possui um script responsável por preparar dados provenientes de uma planilha de estoque.

O fluxo atual realiza:

```text
Planilha
   ↓
Pandas
   ↓
Limpeza dos dados
   ↓
Separação de modelo e tamanho
   ↓
Validação
   ↓
Consolidação dos produtos
   ↓
Preparação para SQLite
```

Produtos que possuem registros diferentes na base, mas representam o mesmo modelo e tamanho, são consolidados para que o sistema trabalhe com o saldo físico total.

## Tecnologias utilizadas

- Python
- Flask
- Pandas
- SQLite / SQL
- HTML
- CSS
- Git
- GitHub

## Estrutura do projeto

```text
projeto-excessos-estoque/
│
├── app.py
├── importar_estoque.py
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── consulta.html
├── .gitignore
└── README.md
```

## Privacidade dos dados

Os arquivos utilizados como fonte de dados durante o desenvolvimento não são disponibilizados neste repositório.

Planilhas de estoque e o banco de dados local são ignorados pelo Git para evitar a publicação de informações provenientes do ambiente real utilizado como referência para o projeto.

Futuramente, uma base fictícia poderá ser utilizada para permitir a demonstração completa da importação sem expor dados reais.

## Status do projeto

Em desenvolvimento

Atualmente, o projeto já possui controle básico de entrada e saída com SQLite e um processo separado de tratamento da planilha de estoque.

A próxima etapa é integrar os dados tratados ao banco SQLite e utilizá-los na página de consulta de estoque.

## Próximas etapas

- Sincronizar os dados tratados com o SQLite
- Exibir os produtos e quantidades na página de consulta
- Desenvolver pesquisa e filtros de produtos
- Implementar autocomplete na busca
- Melhorar a interface da consulta de estoque
- Evoluir as validações e mensagens para o usuário
- Criar uma base fictícia para demonstração pública