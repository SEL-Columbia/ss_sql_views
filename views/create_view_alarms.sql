create view view_alerts as
select distinct
       a.date,
       a.type,
       a.meter_id,
       a.circuit_id,
       c.ip_address,
       c.pin,
       m.name as meter_name
from alerts as a
join meter as m
on meter_id=m.id
join circuit as c
on a.circuit_id=c.id
;