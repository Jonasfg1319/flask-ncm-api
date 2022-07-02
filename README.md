# flask-ncm-api
Api para consultar os novos ncms que a sefaz atualizou em 2022

link https://consulta-ncm.herokuapp.com/

Essa api foi construida para ajudar na demanda de clientes de comércio que ainda tem em seus respectivos sistemas, ncms antigos que ainda não foram atualizados.

A api é bem simples, mas antes de construir a aplicação, foi necessário cadastrar todos os ncms que estão no pdf da sefaz. Isso seria inviável para fazer manualmente, por isso foi desenvolvido o pequeno script para inserção autamatica na base de dados.

O pdf da sefaz foi convertido em arquivo texto, para simplificar o processo (o txt está disponivel na pasta insert_database/ncms.txt). O script desenvolvido lê o arquivo ncms.txt e converte tudo em tabelas no banco de dados de forma mais dinamica. 

