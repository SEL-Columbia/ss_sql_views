-- this view creates a listing of dates at which the watthours have decreased

drop view view_watthour_drops;

create view view_watthour_drops as
select * from (
    select
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
    where
        meter_timestamp > '2011-11-01'
        and meter_timestamp < '2011-12-01'
    order by
        meter_timestamp

) as q
where
    power<0
    and extract(hour from meter_timestamp)=1
;