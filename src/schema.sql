drop table if exists room;

CREATE TABLE room (
       name text not null,
       city text not null, 
       site text, 
       building text not null, 
       wing text,
       floor text not null, 
       comment text
);

CREATE INDEX nameindex on room(name);
