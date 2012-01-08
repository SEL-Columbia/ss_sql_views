-- creates view that calculates hourly averaged power
-- currently does not properly account for midnight reset

drop view view_power;

create view view_power as
select
    *
from
    (select
        meter_timestamp,
        watthours,
        meter_name,
        ip_address,
        watthours - lag(watthours,1)
            over (partition by ip_address, meter_name
            order by meter_timestamp)
            as power,
        meter_timestamp - lag(meter_timestamp, 1)
            over (partition by ip_address, meter_name
            order by meter_timestamp)
            as time_difference
    from
         view_primary_log
    order by
        meter_timestamp)
    as q
    -- how do i deal with midnight stuff?
where
    power > 0
    and time_difference = '01:00:00'
;