drop view view_midnight;

create view view_midnight as
select distinct
       l.date,
       p.circuit_id,
       p.watthours,
       c.ip_address,
       m.name
from primary_log as p
join
  log as l
on
  p.id=l.id
join
     circuit as c
on
	p.circuit_id=c.id
join
    meter as m
on
    c.meter=m.id
where extract(hour from l.date)=0;
