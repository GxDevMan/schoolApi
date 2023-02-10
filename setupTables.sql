CREATE SCHEMA `schoolDb`;

  CREATE TABLE `schoolDb`.`role_table` (
  `role_id` INT NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`role_id`));

  CREATE TABLE `schoolDb`.`user_table` (
  `email` VARCHAR(200) NOT NULL,
  `role_id` INT NOT NULL,
  `phone_number` bigint NOT NULL,
  `first_name` VARCHAR(200) NOT NULL,
  `last_name` VARCHAR(200) NOT NULL,
  `password` VARCHAR(1000) NOT NULL,
  PRIMARY KEY (`email`),
  FOREIGN KEY (`role_id`) REFERENCES `role_table` (`role_id`));

  CREATE TABLE `schoolDb`.`category_table` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`category_id`));

  CREATE TABLE `schoolDb`.`inventory_table` (
  `item_code` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  `item_name` VARCHAR(200) NOT NULL,
  `item_condition` VARCHAR(100) NOT NULL,
  `status` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`item_code`),
  FOREIGN KEY (`category_id`) REFERENCES `category_table` (`category_id`));

CREATE TABLE `schoolDb`.`reservation_table` (
  `reservation_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(200) NOT NULL,
  `item_code` int NOT NULL,
  `data_of_reservation` date NOT NULL,
  `date_of_expiration` date NOT NULL,
  `claim` bool NOT NULL,
  PRIMARY KEY (`reservation_id`),
  FOREIGN KEY (`email`) REFERENCES `user_table` (`email`),
  FOREIGN KEY (`item_code`) REFERENCES `inventory_table` (`item_code`));

  CREATE TABLE `schoolDb`.`history_table` (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(200) NOT NULL,
  `item_code` int NOT NULL,
  `date_in` datetime NOT NULL,
  `date_out`datetime NULL,
  `due_date` DATE NOT NULL,
  `notes` varchar(200) NOT NULL,
  PRIMARY KEY (`history_id`),
  FOREIGN KEY (`email`) REFERENCES `user_table` (`email`),
  FOREIGN KEY (`item_code`) REFERENCES `inventory_table` (`item_code`));

Insert into schooldb.role_table (role_id, role_name) values('User');
Insert into schooldb.role_table (role_id, role_name) values('Admin');
Insert into schooldb.role_table (role_id, role_name) values('Editor');