-- creates view that calculates hourly averaged power
-- currently does not properly account for midnight reset

drop view view_solar_power;

create view view_solar_power as
select
    *
from
    (select
        meter_timestamp,
        solar_kwh,
        battery_volts,
        meter_name,
        solar_kwh - lag(solar_kwh, 1)
            over (partition by meter_name
            order by meter_timestamp)
            as power,
        meter_timestamp - lag(meter_timestamp, 1)
            over (partition by meter_name
            order by meter_timestamp)
            as time_difference
    from
         view_solar
    order by
        meter_timestamp)
    as q
    -- how do i deal with midnight stuff?
where
    time_difference = '01:00:00'
;