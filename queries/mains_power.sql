-- queries power for mains circuit

select
	*
from
	view_power
where
	meter_name = 'ml03'
	and ip_address='192.168.1.200'
order by meter_timestamp

;