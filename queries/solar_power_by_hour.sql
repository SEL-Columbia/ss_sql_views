select 
       avg(power), 
       count(power), 
       meter_name, 
       extract(hour from meter_timestamp)
from 
     view_solar_power 
group by
      meter_name,
      extract(hour from meter_timestamp)
order by
      meter_name,
      extract(hour from meter_timestamp)
;
