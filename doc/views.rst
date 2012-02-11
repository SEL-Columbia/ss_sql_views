Views
=====


view_primary_log
----------------

This view joins four tables to allow a query of watthours that includes
the customer information.


view_power
----------

File to create is create_view_power.sql

This view uses view_primary_log and the lag function to calculate
the change in watthours over two neighboring values separated by
a single hour.


view_solar_power
----------------

view_recharge
-------------

Contains a join that allows us to look at commerce activity.


view_solar
----------


create_view_meter.sql
---------------------


create_view_midnight.sql
------------------------



create_view_primary_log.sql
create_view_recharge.sql
create_view_solar.sql
create_view_solar_midnight.sql
create_view_solar_power.sql
create_view_watthour_drops.sql

create_views.sql
----------------
deprecated
