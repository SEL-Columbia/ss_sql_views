-- this view creates a primary log table for better human parsing

--drop view view_primary_log cascade;

create view view_primary_log as
select distinct
       l.date as meter_timestamp,
       p.created as gateway_timestamp,
       p.circuit_id,
       p.watthours,
       p.credit,
       c.ip_address,
       c.pin,
       m.name as meter_name
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
    c.meter=m.id;
