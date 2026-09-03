# Projeto Excessos do Estoque

Aplicação web desenvolvida para praticar conceitos de desenvolvimento front-end, back-end, tratamento de dados, banco de dados e deploy através de um sistema de controle e consulta de estoque.

## Sobre o projeto

A ideia deste projeto surgiu a partir da observação de uma necessidade real no ambiente de varejo: facilitar o registro de entradas e saídas de produtos excedentes do estoque e permitir uma consulta simples das quantidades disponíveis.

O sistema permite que vendedores e assistentes registrem movimentações informando modelo, tamanho, tipo de movimentação e quantidade.

Além das movimentações, a aplicação utiliza dados provenientes de uma planilha de estoque no formato `.xlsb`. Esses dados são tratados com Python e Pandas antes de serem sincronizados com um banco PostgreSQL.

A aplicação está atualmente hospedada no Render e utiliza um banco PostgreSQL hospedado no Neon.

O projeto continua em desenvolvimento e faz parte do meu processo de aprendizado em programação, análise de dados e desenvolvimento de aplicações web com Python.

## Funcionalidades atuais

- Formulário para registro de movimentações de estoque
- Registro de entradas e saídas
- Controle por modelo, tamanho e quantidade
- Comunicação entre formulários HTML e back-end Flask
- Processamento dos dados enviados pelos formulários
- Importação de dados utilizando Pandas
- Leitura de arquivos `.xlsb`
- Tratamento e validação de modelos, tamanhos e quantidades
- Agrupamento de registros por modelo e tamanho
- Sincronização dos dados com PostgreSQL
- Inserção de novos produtos
- Atualização das quantidades de produtos existentes
- Remoção de registros que não estão mais presentes na fonte de dados
- Consulta dos produtos através da aplicação Flask
- Pesquisa de estoque pelo nome do modelo
- Busca parcial de modelos
- Agrupamento dos resultados por modelo e variação
- Identificação das grades de tamanhos
- Tratamento de grades especiais para determinados modelos
- Navegação entre movimentação e consulta de estoque
- Interface adaptada para computadores e celulares
- Aplicação publicada na web através do Render
- Banco de dados PostgreSQL hospedado no Neon

## Arquitetura atual

Atualmente, o projeto utiliza serviços separados para código, aplicação e banco de dados.

```text
GitHub
   |
   | código-fonte
   v
Render
   |
   | Flask / Python
   |
   | DATABASE_URL
   v
Neon
   |
   v
PostgreSQL
```

O Render é responsável pela execução da aplicação Flask.

O Neon é responsável pelo armazenamento persistente dos dados através do PostgreSQL.

A aplicação utiliza a variável de ambiente `DATABASE_URL` para estabelecer a conexão com o banco sem armazenar credenciais diretamente no código-fonte.

## Fluxo dos dados

O estoque utilizado pela aplicação é obtido inicialmente através de uma planilha no formato `.xlsb`.

O processo de atualização segue aproximadamente este fluxo:

```text
Sistema Estoque.xlsb
        |
        v
      Pandas
        |
        v
Tratamento dos dados
        |
        v
Agrupamento
Modelo + Tamanho
        |
        v
importar_estoque.py
        |
        v
Neon PostgreSQL
        |
        v
Flask no Render
        |
        v
Página de consulta
```

Durante o tratamento são utilizadas principalmente as informações:

- Modelo
- Tamanho
- Quantidade física

A descrição original dos produtos contém informações de modelo e tamanho. O script separa essas informações e converte os valores para os formatos necessários.

Registros correspondentes ao mesmo modelo e tamanho são agrupados para consolidar suas quantidades.

Depois do tratamento, os registros são sincronizados com o PostgreSQL.

## Sincronização do estoque

A atualização dos dados é realizada através do script:

```text
importar_estoque.py
```

O script:

1. lê `Sistema Estoque.xlsb`;
2. acessa a base de dados necessária;
3. trata os nomes dos produtos;
4. separa modelo e tamanho;
5. valida os valores;
6. agrupa registros correspondentes ao mesmo modelo e tamanho;
7. conecta ao PostgreSQL;
8. sincroniza os produtos com o banco.

A sincronização utiliza uma combinação única de:

```text
Modelo + Tamanho
```

Quando um registro já existe, sua quantidade é atualizada.

Quando não existe, um novo registro é criado.

Produtos que não estão mais presentes nos dados processados também podem ser removidos durante a sincronização.

## Consulta de estoque

A aplicação possui uma página dedicada à consulta dos produtos armazenados no banco.

Em vez de exibir todos os registros de estoque de uma única vez, o usuário pode pesquisar pelo nome ou por parte do nome de um modelo.

Por exemplo:

```text
V-90
```

A pesquisa pode retornar diferentes variações desse modelo.

Os resultados são organizados por modelo e seus respectivos tamanhos, facilitando a consulta do estoque.

O sistema também possui tratamento de grades para identificar os tamanhos esperados de determinados produtos.

Alguns modelos possuem regras específicas de grade, enquanto categorias como produtos Baby, Small e acessórios possuem tratamentos próprios.

## Banco de dados

O projeto utiliza atualmente:

**PostgreSQL**

O banco de produção está hospedado no Neon e é acessado pela aplicação Flask através da variável de ambiente:

```text
DATABASE_URL
```

A aplicação utiliza operações SQL como:

- `SELECT` para consulta
- `INSERT` para inclusão
- `UPDATE` para alteração das quantidades
- `DELETE` para remoção de registros

A combinação entre modelo e tamanho possui uma restrição `UNIQUE`, evitando registros duplicados dessa combinação.

Durante a sincronização do estoque também é utilizado:

```sql
ON CONFLICT
```

permitindo atualizar registros existentes sem criar duplicações.

## Deploy

A aplicação Flask está hospedada no Render.

A arquitetura de produção é:

```text
Usuário
   |
   v
Render
   |
   v
Flask
   |
   v
DATABASE_URL
   |
   v
Neon PostgreSQL
```

As credenciais do banco não são armazenadas diretamente no código.

A conexão é configurada através das variáveis de ambiente do serviço de hospedagem.

## Segurança das informações

Arquivos e informações que não devem fazer parte do repositório público são ignorados através do `.gitignore`.

Entre eles:

```text
.env
Sistema Estoque.xlsb
estoque.db
.venv/
venv/
__pycache__/
```

Dessa forma, credenciais locais, ambientes virtuais, arquivos de estoque e bancos utilizados durante etapas anteriores do desenvolvimento não são enviados ao GitHub.

## Imagens dos produtos

As imagens utilizadas durante o desenvolvimento servem apenas como demonstração visual.

A aplicação não utiliza imagens oficiais ou proprietárias diretamente no repositório público.

Em uma implementação futura, poderão ser utilizadas imagens próprias, autorizadas ou provenientes de uma integração oficial.

## Tecnologias utilizadas

- Python
- Flask
- Pandas
- PostgreSQL
- Psycopg
- SQL
- HTML
- CSS
- Jinja
- Gunicorn
- Git
- GitHub
- Render
- Neon

## Estrutura do projeto

```text
projeto-excessos-estoque/
|
|-- app.py
|-- importar_estoque.py
|-- requirements.txt
|
|-- static/
|   `-- style.css
|
|-- templates/
|   |-- index.html
|   `-- consulta.html
|
|-- .gitignore
`-- README.md
```

Arquivos utilizados somente localmente, como `Sistema Estoque.xlsb`, não fazem parte do repositório público.

## Desenvolvimento local

Durante o desenvolvimento, a aplicação Flask pode ser executada utilizando:

```bash
flask --app app run --debug
```

O modo debug permite que alterações salvas durante o desenvolvimento sejam recarregadas automaticamente.

A conexão com o PostgreSQL é definida através da variável de ambiente `DATABASE_URL`.

## Objetivo de aprendizado

Este projeto funciona também como um ambiente prático de estudo.

Durante seu desenvolvimento foram aplicados conceitos relacionados a:

- Programação em Python
- Manipulação e tratamento de dados com Pandas
- PostgreSQL
- Consultas SQL
- Integração com banco de dados remoto
- Desenvolvimento back-end com Flask
- Templates com Jinja
- HTML e CSS
- Responsividade
- Variáveis de ambiente
- Deploy de aplicações
- Git e GitHub
- Estruturação de projetos
- Integração entre front-end, back-end e banco de dados

## Próximos passos

O projeto continuará sendo utilizado como ambiente de aprendizado e evolução.

Entre os próximos estudos e melhorias estão:

- JavaScript
- Manipulação do DOM
- Eventos e interações no front-end
- Integração entre JavaScript e Flask
- Desenvolvimento de APIs
- Consumo de APIs com `fetch`
- React
- Evolução da interface e experiência de uso

## Status do projeto

**Em desenvolvimento — aplicação publicada e banco de produção configurado.**

A estrutura principal do sistema está funcional, incluindo movimentações, consulta de estoque, tratamento de dados, sincronização com PostgreSQL e deploy da aplicação.