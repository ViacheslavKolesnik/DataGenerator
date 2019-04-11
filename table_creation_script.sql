CREATE DATABASE IF NOT EXISTS `simcord`;
USE `simcord`;
DROP TABLE IF EXISTS `order`;

CREATE TABLE `order` (
  `id` bigint(20) NOT NULL,
  `order_id` varchar(20) NOT NULL,
  `cur_pair` varchar(12) NOT NULL,
  `direction` varchar(5) NOT NULL,
  `status` varchar(15) NOT NULL,
  `datetime` bigint(13) NOT NULL,
  `init_px` decimal(20,5) NOT NULL,
  `fill_px` decimal(20,5) NOT NULL,
  `init_vol` decimal(20,8) NOT NULL,
  `fill_vol` decimal(20,8) NOT NULL,
  `description` varchar(45) NOT NULL,
  `tag` varchar(12) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
