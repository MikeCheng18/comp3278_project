DROP DATABASE IF EXISTS iKYC;
CREATE DATABASE iKYC;
use iKYC;

ALTER DATABASE iKYC CHARACTER SET utf8 COLLATE utf8_general_ci;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+08:00";

DROP TABLE IF EXISTS `Customer`;
CREATE TABLE `Customer` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`username`)
);

INSERT INTO `Customer` (`username`,`password`) VALUES
  ("amy", 'amy');

DROP TABLE IF EXISTS `LoginHistory`;
CREATE TABLE `LoginHistory` (
  `username` varchar(50) NOT NULL,
  `login_time` time NOT NULL,
  `login_date` date NOT NULL
);

INSERT INTO `LoginHistory` (`username`,`login_time`,`login_date`) VALUES
  ("amy",  NOW(), '2021-09-01'),
  ("amy",  NOW(), '2021-09-02'),
  ("amy",  NOW(), '2021-09-03');

DROP TABLE IF EXISTS `Currency`;
CREATE TABLE `Currency` (
  `currency_id` varchar(5) NOT NULL, -- USD / HKD / RMB
  `interest_rate` float(6,4) DEFAULT NULL,
  `exchange_rate` float(10,7) DEFAULT NULL, -- exchange with USD
  PRIMARY KEY (`currency_id`)
);

INSERT INTO `Currency` (`currency_id`,`interest_rate`,`exchange_rate`) VALUES
  ("USD", 1.1, 1),
  ("HKD", 1.2, 0.13),
  ("RMB", 1.3, 0.16),
  ("EUR", 1.3, 1.15),
  ("GBP", 1.2, 1.34),
  ("SGD", 1.1, 0.74);

DROP TABLE IF EXISTS `Account`;
CREATE TABLE `Account` (
  `account_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `currency` varchar(5) NOT NULL,
  `balance` float(32,4) DEFAULT NULL,
  `type` varchar(1) NOT NULL, -- s:savning ; c:current
  PRIMARY KEY (`account_id`)
);

INSERT INTO `Account` (`username`,`currency`,`balance`, `type`) VALUES
  ("amy", "HKD", 214, 's'),
  ("amy", "HKD", 1314, 'c'),
  ("amy", "USD", 520, 'c'),
  ("amy", "RMB", 999, 'c');

DROP TABLE IF EXISTS `Transaction`;
CREATE TABLE `Transaction` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `from_Customer_id` VARCHAR(16),
  `to_Customer_id` VARCHAR(16),
  `amount` float(32,4) DEFAULT NULL, -- based on to_Customer_id
  `trans_date` date NOT NULL,
  `trans_time` time NOT NULL,
  `msg` varchar(200) NOT NULL,
  PRIMARY KEY (`transaction_id`)
);

INSERT INTO `Transaction` (`from_Customer_id`,`to_Customer_id`,`amount`,`trans_date`,`trans_time`,`msg`) VALUES
  ("000001", "000002", 5.2, '2021-09-08', NOW(), 'To my current account'),
  ("000002", "000001", 10.4, '2021-09-07', NOW(), 'To my saving account'),
  ("000001", "000002", 4.3, '2021-09-01', NOW(), 'To my current account'),
  ("000002", "000001", 8.4, '2021-09-02', NOW(), 'To my saving account'),
  ("000001", "000003", 10.4, '2021-09-06', NOW(), 'To my current account'),
  ("000003", "000001", 5.2, '2021-09-05', NOW(), 'To my saving account'),
  ("000001", "000003", 8.4, '2021-09-03', NOW(), 'To my current account'),
  ("000003", "000001", 4.3, '2021-09-04', NOW(), 'To my saving account');