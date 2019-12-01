create table tb_vendas(
	id serial primary key unique,
	id_usuario integer,
	nome_comprador varchar(50),
	data_compra date,
	FOREIGN KEY (id_usuario) REFERENCES tb_usuarios(id)
)

insert into tb_vendas values (default, 1, 'comprador', current_date);

select * from tb_vendas;