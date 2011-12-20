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

drop view view_meter;

create view view_meter as
select
    c.id as circuit_id,
    m.id as meter_id,
    m.name,
    c.ip_address,
    c.pin
from circuit as c
join meter as m
on c.meter=m.id;

drop view view_primary_log;

create view view_primary_log as
select distinct
       l.date,
       p.circuit_id,
       p.watthours,
       p.credit,
       c.ip_address,
       c.pin,
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
    c.meter=m.id;

drop view view_addcredit;

create view view_addcredit as
select
    a.credit     as credit_amount,
    a.token_id   as token_id,
    j.start      as start_date,
    j.end        as end_date,
    m.name       as meter_name,
    c.ip_address as ip_address,
    c.pin        as user_pin
from
    addcredit as a
join
    jobs as j
on
    a.id = j.id
join
    circuit as c
on
    c.id = j.circuit_id
join
    meter as m
on
    c.meter=m.id