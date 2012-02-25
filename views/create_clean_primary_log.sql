drop table clean_primary_log;

create table clean_primary_log
(
meter_timestamp timestamp,
gateway_timestamp timestamp,
circuit_id integer,
watthours double precision,
credit double precision,
ip_address varchar,
pin varchar,
meter_name varchar,
PRIMARY KEY (meter_timestamp,
             ip_address,
             meter_name)
);