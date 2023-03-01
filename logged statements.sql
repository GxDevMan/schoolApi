SELECT * FROM schooldb.user_table;

SELECT inventory_table.item_code ,inventory_table.item_name FROM inventory_table
WHERE NOT EXISTS(
SELECT inventory_table.item_code ,inventory_table.item_name FROM inventory_table 
JOIN reservation_table ON reservation_table.item_code = inventory_table.item_code
WHERE reservation_table.date_of_expiration > CURDATE() AND reservation_table.claim=False)
AND NOT EXISTS(
SELECT inventory_table.item_code ,inventory_table.item_name FROM inventory_table 
JOIN history_table ON history_table.item_code = inventory_table.item_code
WHERE history_table.date_out is NUll) AND inventory_table.status='Available';

SELECT inventory_table.item_code ,inventory_table.item_name FROM inventory_table 
LEFT JOIN reservation_table ON reservation_table.item_code = inventory_table.item_code
LEFT JOIN history_table on history_table.item_code = inventory_table.item_code
WHERE 
reservation_table.date_of_expiration is not null 
AND history_table.date_out is not null; 

SELECT inventory_table.item_code ,inventory_table.item_name FROM inventory_table
JOIN reservation_table ON reservation_table.item_code = inventory_table.item_code
WHERE reservation_table.item_code is null;


SELECT inventory_table.item_code ,inventory_table.item_name FROM inventory_table 
JOIN reservation_table ON reservation_table.item_code = inventory_table.item_code 
WHERE reservation_table.date_of_expiration > CURDATE();

SELECT inventory_table.item_code ,inventory_table.item_name FROM inventory_table 
JOIN history_table ON history_table.item_code = inventory_table.item_code
WHERE history_table.date_out is null; 


Drop table history_table;
Drop table reservation_table;
Drop table inventory_table;
Drop table category_table;
Drop table user_table;

