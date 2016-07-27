drop table IF EXISTS email;
create table IF NOT EXISTS email 
(id text,
 name   text,
 email text,
 subject text,
 msg     text,
 sent    datetime);

insert into email (id,name,email,subject,msg)
 values ('6efce068-5336-11e6-bef4-a0999b19ce1b','Mike','mchirico@gmail.com','Sample "test" message2','Hi Mike:

This is a sample message. You''ll have to figure out
how to deal with quotes. Here''s an example of
something "quoted."

Regards,
Piggy');
insert into email (id,name,email,subject,msg)
  values ('4efa18e8-5337-11e6-94f8-a0999b19ce1b','Mike','mike.chirico@cwxstat.com','Sample "test" message','Hi Mike:\n\n This is a sample message.\n\nRegards,\n\nPiggy');

