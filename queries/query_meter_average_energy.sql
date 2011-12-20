select to_char(avg(sq.watthours), '9999.9'), count(sq.watthours), sq.circuit_id
from

(select distinct date, watthours, primary_log.circuit_id
from primary_log, log
where primary_log.circuit_id
in

(select id from circuit where meter=19)

and log.date>'2011-10-1'
and log.date<='2011-10-26'
and extract(hour from date)=0
and primary_log.id=log.id
) as sq

group by sq.circuit_id
order by sq.circuit_id
;


