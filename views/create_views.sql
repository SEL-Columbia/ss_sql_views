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