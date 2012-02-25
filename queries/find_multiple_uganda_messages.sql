select 
	extract(year from created),
	extract(month from created),
	extract(day from created),
	circuit_id,
	count(watthours)
from
primary_log
where 
	created > '2012-01-01' 
	and
	created < '2012-01-07'
group by
extract(day from created),
extract(month from created),
extract(year from created),
circuit_id
order by
extract(year from created),
extract(month from created), 
extract(day from created),
circuit_id
;