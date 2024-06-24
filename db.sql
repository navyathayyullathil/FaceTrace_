/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - attendance_face
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`attendance_face` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `attendance_face`;

/*Table structure for table `absent_noti` */

DROP TABLE IF EXISTS `absent_noti`;

CREATE TABLE `absent_noti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `absent_noti` */

/*Table structure for table `attendence` */

DROP TABLE IF EXISTS `attendence`;

CREATE TABLE `attendence` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `studentlid` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `attendance` int(10) DEFAULT NULL,
  `image` varchar(45) DEFAULT NULL,
  `hour` varchar(45) DEFAULT NULL,
  `sem` varchar(54) DEFAULT NULL,
  `division` varchar(44) DEFAULT NULL,
  `department` varchar(44) DEFAULT NULL,
  `subid` int(11) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=latin1;

/*Data for the table `attendence` */

insert  into `attendence`(`aid`,`studentlid`,`date`,`attendance`,`image`,`hour`,`sem`,`division`,`department`,`subid`,`status`) values 
(1,3,'2024-03-14',1,'s3','1','1','A','CSE',2,'notify'),
(2,4,'2024-03-14',0,'s3','1','1','A','CSE',2,'notify'),
(3,8,'2024-03-14',0,'s3','1','1','A','CSE',2,'viewed'),
(4,9,'2024-03-14',0,'s3','1','1','A','CSE',2,'notify'),
(5,11,'2024-03-14',1,'s3','1','1','A','CSE',4,'notify'),
(6,11,'2024-03-13',1,'s3','2','1','A','CSE',4,'notify'),
(7,11,'2024-03-12',1,'s3','3','1','A','CSE',5,'notify'),
(8,11,'2024-03-09',0,'s3','4','1','A','CSE',5,'notify'),
(9,11,'2024-03-09',0,'s3','5','1','A','CSE',5,'notify'),
(11,11,'2024-03-11',0,'s3','7','1','A','CSE',5,'notify'),
(12,9,'2024-03-14',0,'s3','1','1','A','CSE',2,'notify'),
(13,9,'2024-03-13',0,'s3','2','1','A','CSE',2,'notify'),
(14,9,'2024-03-12',0,'s3','3','1','A','CSE',2,'notify'),
(15,9,'2024-03-28',0,'sw','4','1','A','CSE',2,'notify'),
(16,9,'2024-03-19',0,'s3','6','1','A','CSE',2,'notify'),
(17,9,'2024-03-20',0,'s3','5','1','A','CSE',2,'notify'),
(22,9,'2024-03-15',1,'s9','1','1','A','CSE',1,'notify'),
(23,8,'2024-03-15',0,'s3','1','1','A','CSE',3,'notify'),
(24,8,'2024-03-15',1,'s3','1','1','A','CSE',3,'notify'),
(25,8,'2024-03-15',1,'s3','1','1','A','CSE',3,'notify'),
(26,8,'2024-03-16',0,'s11','1','1','A','CSE',3,'notify'),
(28,11,'2024-03-25',1,'s11','1','1','A','CSE',3,'notify'),
(29,8,'2024-03-25',0,'s(8,)','1','1','A','CSE',3,'notify'),
(30,8,'2024-03-25',0,'s(9,)','1','1','A','CSE',3,'notify'),
(31,8,'2024-03-25',0,'s(10,)','1','1','A','CSE',3,'notify'),
(32,8,'2024-03-25',0,'s(10,)','1','1','A','CSE',3,'notify'),
(33,8,'2024-03-25',0,'s(10,)','1','1','A','CSE',3,'notify'),
(34,8,'2024-03-25',0,'s(10,)','1','1','A','CSE',3,'notify'),
(35,8,'2024-03-25',0,'s(10,)','1','1','A','CSE',3,'notify'),
(36,11,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(37,11,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(38,11,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(39,11,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(40,11,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(41,11,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(42,11,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(43,8,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(44,8,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(45,8,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(46,8,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(47,8,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(48,8,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(49,8,'2024-03-27',0,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(50,9,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(51,9,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(52,9,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(53,9,'2024-03-27',0,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(54,9,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(55,9,'2024-03-27',0,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(56,9,'2024-03-27',0,'s(10,)','1','1','A','CSE',3,'notify'),
(60,11,'2024-03-19',0,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(61,11,'2024-03-19',0,'s(10,)','1','1','A','CSE',3,'notify'),
(62,11,'2024-03-19',0,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(63,11,'2024-03-19',1,'s(10,)','1','1','A','CSE',3,'notify'),
(64,11,'2024-03-19',1,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(65,11,'2024-03-19',1,'s(10,)','1','1','A','CSE',3,'notify'),
(66,11,'2024-03-19',1,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(67,9,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'notify'),
(68,9,'2024-03-12',0,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(69,9,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'notify'),
(70,9,'2024-03-12',0,'s(10,)','1','1',NULL,'CSE',3,'notify'),
(71,9,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'notify'),
(72,9,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'notify'),
(73,9,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'notify'),
(74,11,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'viewed'),
(75,11,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'notify'),
(76,11,'2024-03-12',0,NULL,'1','1','A','CSE',3,'viewed'),
(77,11,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'notify'),
(78,11,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'viewed'),
(79,11,'2024-03-12',0,NULL,'1','1','A','CSE',3,'notify'),
(80,11,'2024-03-12',0,'s(10,)','1','1','A','CSE',3,'notify'),
(81,10,'2024-03-20',1,NULL,'1','1','A','CSE',3,'notify'),
(92,10,'2024-03-27',1,NULL,'1','1','A','CSE',3,'viewed'),
(93,10,'2024-03-27',1,'s(10,)','1','1','A','CSE',3,'notify'),
(94,10,'2024-03-27',1,NULL,'1','1','A','CSE',3,'viewed'),
(95,9,'2024-03-23',1,'s(10,)','1','1','A','CSE',3,'notify'),
(96,9,'2024-03-23',1,NULL,'1','1','A','CSE',3,'notify'),
(97,9,'2024-03-23',1,'s(10,)','1','1','A','CSE',3,'notify'),
(98,9,'2024-03-23',1,NULL,'1','1','A','CSE',3,'notify'),
(99,9,'2024-03-23',1,'s(10,)','1','1','A','CSE',3,'notify'),
(100,9,'2024-03-23',0,NULL,'1','1','A','CSE',3,NULL),
(101,9,'2024-03-23',1,'s(10,)','1','1','A','CSE',3,'notify'),
(105,2,'2024-04-20',0,'s2','1','1','A','CSE',3,'notify'),
(106,8,'2024-04-20',0,'s(10,)','1','1','A','CSE',3,'notify'),
(107,9,'2024-04-20',0,'s9','1','1','A','CSE',3,'notify'),
(108,10,'2024-04-20',0,'s(10,)','1','1','A','CSE',3,'notify'),
(109,11,'2024-04-20',0,'s11','1','1','A','CSE',3,'notify'),
(110,12,'2024-04-25',0,'s(10,)','1','1','A','CSE',3,'notify'),
(111,8,'2024-04-25',0,'s8','1','1','A','CSE',3,'notify'),
(112,9,'2024-04-25',0,'s(10,)','1','1','A','CSE',3,'notify'),
(114,11,'2024-04-25',0,'s(10,)','1','1','A','CSE',3,'notify'),
(115,12,'2024-04-25',0,'s12','2','1','A','CSE',3,'notify'),
(116,8,'2024-04-25',0,'s(10,)','2','1','A','CSE',3,'notify'),
(117,9,'2024-04-25',0,'s9','2','1','A','CSE',3,'notify'),
(119,11,'2024-04-25',0,'s11','2','1','A','CSE',3,'notify'),
(124,0,'2024-04-25',1,'s(10,)','2','1','A','CSE',3,'notify');

/*Table structure for table `images` */

DROP TABLE IF EXISTS `images`;

CREATE TABLE `images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `logid` int(11) DEFAULT NULL,
  `image` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=latin1;

/*Data for the table `images` */

insert  into `images`(`id`,`logid`,`image`) values 
(11,11,'20240325_1538041.jpg'),
(12,11,'20240325_1538042.jpg'),
(13,11,'20240325_1538043.jpg'),
(14,11,'20240325_1538044.jpg'),
(15,11,'20240325_1538045.jpg'),
(16,11,'20240325_1538046.jpg'),
(17,11,'20240325_1538057.jpg'),
(18,11,'20240325_1538058.jpg'),
(19,11,'20240325_1538059.jpg'),
(20,11,'20240325_15380510.jpg');

/*Table structure for table `leave` */

DROP TABLE IF EXISTS `leave`;

CREATE TABLE `leave` (
  `lvid` int(11) NOT NULL AUTO_INCREMENT,
  `req_date` varchar(44) DEFAULT NULL,
  `studlid` int(11) DEFAULT NULL,
  `leave` text,
  `days` varchar(55) DEFAULT NULL,
  `leave_date` varchar(55) DEFAULT NULL,
  `status` varchar(44) DEFAULT NULL,
  PRIMARY KEY (`lvid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `leave` */

insert  into `leave`(`lvid`,`req_date`,`studlid`,`leave`,`days`,`leave_date`,`status`) values 
(1,'2024-03-08',4,'kkk','1','2024-02-01','accepted'),
(2,'2024-03-09',9,'fever','6','2024-03-01','pending'),
(3,'2024-03-09',10,'Fever','7','2024-03-03','rejected'),
(5,'2024-03-22',11,'mmmmmmmmmmmmmm','1','2024-03-29','pending');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `usertype` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'annu','123','teacher'),
(3,'deva','1234','teacher'),
(4,'deva','123','student'),
(5,'kiran','123','teacher'),
(6,'siva','123','teacher'),
(7,'deva','123','teacher'),
(8,'yelna','yelna','student'),
(9,'navya','navya','student'),
(10,'sharmmada','sharmmada','student'),
(11,'rinju','123','student');

/*Table structure for table `student` */

DROP TABLE IF EXISTS `student`;

CREATE TABLE `student` (
  `stid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `name` varchar(55) DEFAULT NULL,
  `regno` varchar(55) DEFAULT NULL,
  `address` text,
  `phone` bigint(20) DEFAULT NULL,
  `email` varchar(55) DEFAULT NULL,
  `dob` varchar(55) DEFAULT NULL,
  `department` varchar(55) DEFAULT NULL,
  `semester` int(11) DEFAULT NULL,
  `division` varchar(55) DEFAULT NULL,
  `photo` varchar(55) DEFAULT NULL,
  `gname` varchar(45) DEFAULT NULL,
  `gnumber` varchar(54) DEFAULT NULL,
  PRIMARY KEY (`stid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `student` */

insert  into `student`(`stid`,`lid`,`name`,`regno`,`address`,`phone`,`email`,`dob`,`department`,`semester`,`division`,`photo`,`gname`,`gnumber`) values 
(3,8,'Yelna Mary','JEC20CS126','Muttath(House)',7896660594,'yelnamry@gmail.com','2002-10-03','CSE',1,'B','20240314_235010.jpg','Joseph','674538902'),
(4,9,'Navya T','JEC20CS082','Haripriya',1247887777,'navyaabh@gmail.com','2002-04-02','CSE',1,'B','20240309_133106.jpg','Gaudhami','1234321357'),
(5,10,'Sharmmada A','JEC20CS114','Tulasi',1234567895,'sharmmada@gmail.com','2004-02-13','CSE',1,'B','20240314_235037.jpg','Ajith','6789054321'),
(6,11,'Rinju p','JEC20CS116','pattayil house',9911229900,'rinju@gmail.com','1995-04-22','CSE',1,'A','20240315_103940.jpg','sayooj c','9944991122');

/*Table structure for table `subject` */

DROP TABLE IF EXISTS `subject`;

CREATE TABLE `subject` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(45) DEFAULT NULL,
  `code` varchar(45) DEFAULT NULL,
  `department` varchar(45) DEFAULT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `staff_lid` int(11) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `subject` */

insert  into `subject`(`sid`,`subject`,`code`,`department`,`semester`,`staff_lid`) values 
(3,'os','123','CSE','1',2),
(4,'me','555','CSE','1',6),
(5,'se','666','CSE','1',7);

/*Table structure for table `teacher` */

DROP TABLE IF EXISTS `teacher`;

CREATE TABLE `teacher` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `name` varchar(55) DEFAULT NULL,
  `teacher_code` varchar(33) DEFAULT NULL,
  `address` text,
  `phone` bigint(20) DEFAULT NULL,
  `email` varchar(55) DEFAULT NULL,
  `qualification` varchar(55) DEFAULT NULL,
  `department` varchar(55) DEFAULT NULL,
  `photo` varchar(55) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `teacher` */

insert  into `teacher`(`tid`,`lid`,`name`,`teacher_code`,`address`,`phone`,`email`,`qualification`,`department`,`photo`) values 
(1,2,'annnn marry','123809','pattayil',9911229900,'hema@gmail.com','msc in computer Science','CSE','20240308_224702.jpg'),
(2,3,'devAN','0010','ma',9911229944,'devad@gmail.com','Msc in computer Science','CSE','20240308_224643.jpg'),
(3,5,'KIRAN','333','sdss',9911229933,'kiran@gmail.com','Msc in computer Science','CSE','20240308_224934.jpg'),
(4,6,'sivan','444','qww',9922003344,'sivax@gmail.com','Msc in computer Science','CSE','20240308_225023.jpg'),
(5,7,'deva raj','003','deva raj house',8822000112,'devaraj@gmail.com','msc in computer Science','CSE','20240308_225118.jpg');

/*Table structure for table `timetable` */

DROP TABLE IF EXISTS `timetable`;

CREATE TABLE `timetable` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `dept` varchar(45) DEFAULT NULL,
  `sem` varchar(45) DEFAULT NULL,
  `day` varchar(45) DEFAULT NULL,
  `h1` varchar(56) DEFAULT NULL,
  `h2` varchar(56) DEFAULT NULL,
  `h3` varchar(56) DEFAULT NULL,
  `h4` varchar(50) DEFAULT NULL,
  `h5` varchar(45) DEFAULT NULL,
  `h6` varchar(56) DEFAULT NULL,
  `h7` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `timetable` */

insert  into `timetable`(`tid`,`dept`,`sem`,`day`,`h1`,`h2`,`h3`,`h4`,`h5`,`h6`,`h7`) values 
(1,'CSE','1','Monday','dddd','c++','c++','break','java','c++','java'),
(2,'CSE','1','Tuesday','os','se','me','break','me','java','os'),
(3,'CSE','1','Wednesday','se','java','os','break','se','c++','se'),
(4,'CSE','1','Thursday','java','break','c++','break','c++','os','se'),
(5,'CSE','1','Friday','java','java','c++','break','java','os','c++');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
