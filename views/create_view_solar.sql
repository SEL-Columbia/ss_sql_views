create view view_solar as
select distinct        
       pcu_log.timestamp as meter_timestamp,
       pcu_log.cumulative_khw_solar as solar_kwh,
       pcu_log.battery_volts as battery_volts,
       meter.name as meter_name
from pcu_log
join
	meter
on
	pcu_log.meter_id = meter.id;