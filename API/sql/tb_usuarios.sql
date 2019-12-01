create table tb_usuarios(
	id serial primary key unique,
	nome varchar(20),
	sobrenome varchar(20),
	telefone varchar(20), 
	cpf varchar(20),
	email varchar(50), 
	senha varchar(50)
)

insert into tb_usuarios values (default, 'teste', 'testando', '99999-99999', '123.132.123-80', 'teste@teste.com', 'teste');

select * from tb_usuarios;

