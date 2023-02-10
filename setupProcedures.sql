DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `userInsert`(email varchar(200), pNumber BIGINT, first_name varchar(200), last_name varchar(200), pWord varchar(1000), urole varchar(100))
BEGIN
INSERT INTO `schoolDb`.`user_table` (`email`,  `phone_number`, `first_name`, `last_name`, `password`, `role`) VALUES (email, pNumber, first_name, last_name, pWord, urole);
END //
CREATE DEFINER=`root`@`localhost` PROCEDURE `newCategory`(categoryName varchar(200))
BEGIN
INSERT INTO `schoolDb`.`category_table` (`category_name`) VALUES (categoryName);
END //

CREATE DEFINER=`root`@`localhost` PROCEDURE `newReservation`(email varchar(200), item_code int, expiration_date date, claim tinyint)
BEGIN
INSERT INTO `schoolDb`.`reservation_table` (`email`, `item_code`, `expiration_date`, `claim`) VALUES (email, item_code, expiration_date, claim);
END //

CREATE DEFINER=`root`@`localhost` PROCEDURE `newItem`(roomId INT, item_name varchar(200), item_condition varchar(100), availability varchar(100))
BEGIN
INSERT INTO `schoolDb`.`inventory_table` (`room_id`, `item_name`, `item_condition`, `status`) VALUES (roomId, item_name, item_condition, availability);
END //

CREATE DEFINER=`root`@`localhost` PROCEDURE `historyInsert`(email varchar(200), item_code int, date_in datetime, date_out datetime, notes varchar(200))
BEGIN
	INSERT INTO `schoolDb`.`history_table` (`email`, `item_code`, `date_in`, `date_out`, `notes`) VALUES (email, item_code, date_int, date_out, notes);
END //