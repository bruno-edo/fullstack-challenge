Desafio Full Stack Dev Chaordic
===================

### Dependências do Projeto

- NGINX
- GUnicorn
- Python 3.6
	- Flask 0.12.2
    - short_url 1.2.2
    - sqlite3 (inclusa nas bibliotecas padrão do Python)

Arquitetura
-------------------

Este webservice foi desenvolvido utilizando o micro-framework **Flask**. Os endpoints RESTful são tratados por essa biblioteca Python, enquanto a camada de dados é tratada pelo database engine **SQLite** (integrado aos módulos do Python 3 sob o nome **sqlit3**). Essas duas tecnologias foram escolhidas pela sua simplicidade de desenvolvimento e aplicação, assim diminuindo o tempo de desenvolvimento e facilitando o entendimento do código.


Apesar do **Flask** ter um servidor interno, o uso do mesmo em ambientes de produção não é recomendado. Para solucionar esse problema foi utilizado o stack de tecnologias **NGINX** + **GUnicorn**. O **NGINX** recebe as requisições, encaminha-as ao **GUnicorn**, que por sua vez as entrega ao app **Flask** para processamento.


Funcionamento
-------------------

O tratamento das requisições HTTP se dá da seguinte forma:

1. A requisição é recebida pelo NGINX
2. O NGINX redireciona o tráfego para o endereço localhost:8000
3. Uma instância do GUnicorn capta a requisição e encaminha para o app em Python e
4. O framework Flask encaminha a requisição para o método Python adequado
5. O pedido é processado, e é retornada a resposta adequada a requisição
    - Pedidos que necessitem de acesso ao banco são tratados pela biblioteca sqlite3


Instalação
-------------------

Para instalar a aplicação, e todas as suas dependências, basta apenas rodar o shell script **install.sh**, localizado na pasta **setup**.


Executando a Aplicação
-------------------

Para iniciar os servidores e passar a escutar requisições, basta apenas rodar o shell script **start.sh**, localizado no diretório root deste projeto.

> **Nota**: O script inicia o GUnicorn com 4 workers destinados a aplicação. Caso se deseje alterar esse número, a seguinte linha do arquivo deve ser modificada:
>
> **sudo gunicorn -w 4 -b localhost:8000 main:app**

Testes Automatizados
-------------------
