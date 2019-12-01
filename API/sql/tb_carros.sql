create table tb_carros(
	id serial primary key unique,
	marca varchar(50) ,
	modelo varchar(50),
	ano integer ,
	cor varchar(20),
	valor varchar(50) 
)

insert into tb_carros values(default,'Chevrolet', 'Prisma', 2015, 'Preto', 13.000 );

select * from tb_carros;

