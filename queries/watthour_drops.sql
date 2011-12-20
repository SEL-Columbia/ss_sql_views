-- this query creates a table of watthour decreases that are occurring at unscheduled times

select
	meter_name,
	meter_timestamp,
	ip_address,
	watthours,
	power
from
	view_watthour_drops
where
	meter_timestamp>='2011-12-01'
	and meter_timestamp<'2012-01-01'
	and time_difference='01:00:00'
	and extract(hour from meter_timestamp)!=1
order by
	meter_name,
	meter_timestamp,
	ip_address
;