create table imagenes (
	imagen bytea,
	id varchar(50) PRIMARY KEY
)
--delete from imagenes;
--drop table imagenes

select * from imagenes

SELECT *
    FROM imagenes
    ORDER BY id 
    LIMIT 10 OFFSET 50