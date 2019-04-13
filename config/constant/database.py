ORDER_RECORD_INSERT_PATTERN = "INSERT INTO `order`(id, order_id, cur_pair, direction, status, datetime, init_px, fill_px, init_vol, fill_vol, description, tag) " \
							  "VALUES({0}, '{1}', '{2}', '{3}', '{4}', {5}, {6}, {7}, {8}, {9}, '{10}', '{11}');"
ORDER_RECORD_STATISTICS_SELECT_QUERY = """select 
all_zones.order_records, 
all_zones.orders, 
red_zone.red_zone_orders, 
green_zone. green_zone_orders, 
blue_zone.blue_zone_orders 
from 
( 
	select count(*) as order_records, count(distinct order_id) as orders 
	from `order` 
) as all_zones 
join 
( 
	select count(*) as red_zone_orders 
	from 
		(select order_id from `order` group by order_id) as distinct_order_ids 
		left join 
		(select order_id from `order` where status = 'New') as order_status 
		on distinct_order_ids.order_id = order_status.order_id 
	where order_status.order_id is null 
) as red_zone 
join 
( 
	select count(*) as green_zone_orders 
	from 
		(select order_id, count(order_id) as number_of_records from `order` group by order_id) as records_count 
	where records_count.number_of_records = 3 
) as green_zone 
join 
( 
	select count(*) as blue_zone_orders 
	from 
		(select order_id, count(order_id) as number_of_records from `order` group by order_id) as records_count 
		inner join 
		(select order_id from `order` where status = 'New') as order_status 
		on records_count.order_id = order_status.order_id 
	where records_count.number_of_records = 2 
) as blue_zone;"""
