### Projeto Integrador IV
===

#### Sobre o Projeto Integrador
---------------------
Projeto Integrador IV, do Bacharelado em Ciência da Computação do Centro Universitário Senac - Campus São Paulo. 

O Projeto Integrador IV, tem como objetivo o desenvolvimento de visualizações de dados com informações formuladas com dados extraídos automaticamente de website por meio de sistema de crawling.

#### Funcionamento

####Integrantes
---------------------
##### Alunos:

[Gabriel Fontenelle](https://github.com/OdnaropX)

##### Professor Orientador:

[![cv](http://gediscursivos.files.wordpress.com/2012/12/lattes.png?w=869)](http://lattes.cnpq.br/5909154335340519)  [Profº Marcelo Hashimoto](https://www.github.com/mhsenac)


### Requisitos de instalação
----------------------

Git (opcional recomendado), Python 2.7, PostgreSQL 9.3.

Bibliotecas Python:

Scrapy, Langid

### Utilização
----------------------

Crawler:

Instale o Banco de Dados PostgreSQL e execute os Scripts .sql na pasta requeriments.

Pela linha de comando acesse a pasta crawler e para iniciar o crawling execute o seguinte comando:

scrapy crawl NOME_DO_SPIDER  -s JOBDIR=cache/NOME_DO_SPIDER --logfile=log.log

Onde NOME_DO_SPIDER é um dos spiders disponíveis: myfigure_items, mangaupdates_part1, mangaupdates_part2, mangaupdates_part3, animecharacter_relation, animecharacter_media, animecharacter_character.

Ordem de execução dos spiders:

1 - mangaupdates_part1
2 - mangaupdates_part2
3 - mangaupdates_part3
4 - animecharacter_character
5 - animecharacter_relation
6 - animecharacter_media
7 - myfigure_items

No arquivo "src/crawler/crawler/setting.py" estão as configurações do Banco de Dados e usuário de teste criado para salvar informações dos websites enquanto logado.

Visualização de dados:

O arquivo generator.py possui alguns exemplos de visualização, para gerar visualizações executer o arquivo generator.py. É necessário ter dados no Banco de dados para as visualizações serem geradas. 

####Licença e Créditos
----------------------

Este trabalho foi licenciado sob uma [Licença Creative Commons Atribuição-CompartilhadaIgual 3.0 Brasil.](http://creativecommons.org/choose/results-one?license_code=by-sa&jurisdiction=br&version=3.0&lang=pt_BR)

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License.](http://creativecommons.org/licenses/by-sa/3.0/)

![My image](http://i.creativecommons.org/l/by-sa/3.0/88x31.png)