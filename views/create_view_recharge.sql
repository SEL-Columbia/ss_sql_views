--drop view view_recharge;

create view view_recharge as
select
       jobs.id,
       jobs.state as jobs_state,
       jobs.start,
       jobs.end,
       token.created,
       token.token,
       token.value,
       token.state as token_state,
       circuit.ip_address,
       meter.name
from
     jobs
join
	token
on
	jobs.id = token.id
join
	circuit
on
	jobs.circuit_id = circuit.id
join
	meter
on
	circuit.meter = meter.id
;
