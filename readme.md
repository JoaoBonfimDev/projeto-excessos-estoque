# Projeto Excessos do Estoque

Aplicação web desenvolvida para praticar conceitos de desenvolvimento front-end, back-end, tratamento de dados e banco de dados através de um sistema de controle e consulta de estoque.

## Sobre o projeto

A ideia deste projeto surgiu a partir da observação de uma necessidade real no ambiente de varejo: facilitar o registro de entradas e saídas de produtos excedentes do estoque e permitir uma consulta simples das quantidades disponíveis.

O objetivo é desenvolver uma interface intuitiva para que vendedores e assistentes possam registrar movimentações informando modelo, tamanho, tipo de movimentação e quantidade.

Além das movimentações, o projeto passou a utilizar dados provenientes de uma planilha de estoque, realizando o tratamento dessas informações e armazenando os resultados em um banco de dados local.

O projeto está em desenvolvimento e faz parte do meu processo de aprendizado em programação, análise de dados e desenvolvimento de aplicações com Python.

## Funcionalidades atuais

- Formulário para registro de movimentações de estoque
- Registro de entradas e saídas
- Controle por modelo, tamanho e quantidade
- Comunicação entre formulários HTML e back-end Flask
- Processamento dos dados enviados pelos formulários
- Importação de dados de estoque utilizando Pandas
- Leitura de arquivo no formato `.xlsb`
- Tratamento e validação de modelos, tamanhos e quantidades
- Agrupamento de registros por modelo e tamanho
- Armazenamento dos dados tratados em banco SQLite
- Inserção de novos produtos no banco de dados
- Atualização das quantidades de produtos já existentes
- Consulta dos produtos armazenados no banco através da aplicação Flask
- Pesquisa de estoque por nome do modelo
- Busca parcial de modelos utilizando SQL
- Agrupamento dos resultados por modelo e variação
- Exibição dos tamanhos e respectivas quantidades
- Navegação entre a página de movimentação e a consulta de estoque
- Modelos em destaque na página de consulta
- Interface adaptada para computadores e celulares

## Fluxo dos dados

O estoque utilizado pela aplicação é inicialmente obtido a partir de uma planilha no formato `.xlsb`.

Os dados passam por um processo de tratamento utilizando Pandas, no qual são selecionadas e organizadas as informações necessárias para o sistema, principalmente:

- Modelo
- Tamanho
- Quantidade física

A descrição original dos produtos contém informações de modelo e tamanho. Durante o tratamento, essas informações são separadas e convertidas para formatos adequados antes de serem utilizadas pela aplicação.

Registros correspondentes ao mesmo modelo e tamanho são agrupados, permitindo consolidar suas respectivas quantidades.

Após o tratamento, os dados são sincronizados com um banco de dados SQLite. O sistema verifica se determinado produto já existe no banco para decidir entre inserir um novo registro ou atualizar sua quantidade.

A página de consulta utiliza Flask para acessar essas informações e permite que o usuário pesquise produtos pelo nome do modelo.

Os resultados são agrupados por modelo e variação, exibindo os tamanhos e suas respectivas quantidades.

O fluxo atual pode ser resumido da seguinte forma:

```text
Planilha XLSB
      |
      v
    Pandas
      |
      v
Tratamento dos dados
      |
      v
    SQLite
      |
      v
     Flask
      |
      v
Página de consulta
```

## Consulta de estoque

A aplicação possui uma página dedicada à consulta dos produtos armazenados no banco de dados.

Em vez de exibir todos os registros de estoque de uma única vez, o usuário pode pesquisar pelo nome ou por parte do nome de um modelo.

Por exemplo, uma pesquisa por:

```text
V-90
```

pode retornar diferentes variações desse modelo.

Cada variação é apresentada separadamente, juntamente com seus tamanhos e respectivas quantidades.

Essa estrutura foi desenvolvida para tornar a consulta mais simples e evitar que o usuário precise navegar manualmente por uma grande quantidade de registros.

## Banco de dados

O projeto utiliza SQLite para armazenamento local dos dados tratados.

A aplicação trabalha atualmente com operações como:

- `SELECT` para consulta de produtos
- `INSERT` para inclusão de novos registros
- `UPDATE` para atualização das quantidades
- `DELETE` para remoção de registros quando necessário

O arquivo do banco de dados utilizado durante o desenvolvimento local não é enviado ao repositório.

## Imagens dos produtos

As imagens utilizadas na interface de consulta de estoque são usadas apenas para demonstração visual durante o desenvolvimento local do projeto.

Por esse motivo, a pasta `static/imagens/` não está incluída no repositório e foi adicionada ao `.gitignore`.

O sistema foi estruturado de forma que essas imagens possam ser utilizadas localmente nos cards de produtos sem que os arquivos sejam enviados ao GitHub.

Em uma implementação futura, as imagens poderão ser substituídas por arquivos próprios, imagens autorizadas ou integradas a uma fonte oficial de dados.

## Tecnologias utilizadas

- Python
- Pandas
- Flask
- SQLite
- SQL
- HTML
- CSS
- Jinja
- Git
- GitHub

## Estrutura do projeto

```text
projeto-excessos-estoque/
|
|-- app.py
|-- importar_estoque.py
|-- estoque.db
|-- Sistema Estoque.xlsb
|
|-- static/
|   |-- style.css
|   |
|   `-- imagens/
|
|-- templates/
|   |-- index.html
|   `-- consulta.html
|
|-- .gitignore
`-- README.md
```

Alguns arquivos utilizados localmente, como a planilha de estoque, o banco de dados e as imagens de demonstração, são ignorados pelo Git e não fazem parte do repositório público.

## Arquivos locais

O arquivo `Sistema Estoque.xlsb` utilizado durante o desenvolvimento contém os dados de origem para a importação do estoque e não é enviado ao GitHub.

O arquivo `estoque.db` também é utilizado localmente e não faz parte do repositório.

Esses arquivos estão configurados no `.gitignore`.

## Atualização do estoque

Atualmente, a atualização dos dados é realizada através do script:

```text
importar_estoque.py
```

O script realiza a leitura da planilha, tratamento dos registros e sincronização das informações com o banco SQLite.

Durante o desenvolvimento local, uma nova versão da planilha pode substituir o arquivo anterior mantendo o nome esperado pelo sistema. Ao executar novamente o script de importação, os dados são processados e as quantidades existentes podem ser atualizadas no banco.

Em uma futura implantação da aplicação, o processo de atualização poderá ser adaptado para outras formas de integração, como upload de arquivos, acesso a arquivos compartilhados ou integração com uma fonte oficial de dados.

## Objetivo de aprendizado

Este projeto também funciona como um ambiente prático de estudo.

Durante o desenvolvimento estão sendo aplicados conceitos relacionados a:

- Programação em Python
- Manipulação e tratamento de dados com Pandas
- Banco de dados SQLite
- Consultas SQL
- Desenvolvimento back-end com Flask
- Templates utilizando Jinja
- Desenvolvimento front-end com HTML e CSS
- Integração entre front-end, back-end e banco de dados
- Responsividade
- Controle de versão com Git
- Organização de projetos no GitHub

## Status do projeto

Em desenvolvimento.

Novas funcionalidades e melhorias de interface serão adicionadas conforme o avanço do projeto e dos estudos.