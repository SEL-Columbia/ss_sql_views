drop view view_meter;

create view view_meter as
select
    c.id as circuit_id,
    m.id as meter_id,
    m.name as meter_name,
    c.ip_address,
    c.pin,
    c.energy_max,
    c.power_max,
    c.account_id
from circuit as c
join meter as m
on c.meter=m.id;