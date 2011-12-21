-- query to get average meter energy over a time period

select
    to_char(avg(watthours), '9999.9'),
    count(watthours),
    meter_name
from
    view_primary_log
where
    meter_timestamp > '2011-11-01'
    and meter_timestamp < '2011-12-01'
    and ip_address = '192.168.1.200'
    and extract(hour from meter_timestamp)=0
group by meter_name
order by meter_name
;



