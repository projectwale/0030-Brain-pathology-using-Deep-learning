/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - brainpathology
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`brainpathology` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `brainpathology`;

/*Table structure for table `doctordetails` */

DROP TABLE IF EXISTS `doctordetails`;

CREATE TABLE `doctordetails` (
  `id` int(255) NOT NULL auto_increment,
  `username` varchar(255) default NULL,
  `email` varchar(255) default NULL,
  `phone` varchar(255) default NULL,
  `specialist` varchar(255) default NULL,
  `password` varchar(255) default NULL,
  `filename` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `doctordetails` */

insert  into `doctordetails`(`id`,`username`,`email`,`phone`,`specialist`,`password`,`filename`) values (1,'stawar','stawar59@gmail.com','2165121316','Brain Pathology','s','static/doctor\\banner.png');

/*Table structure for table `patientsrequest` */

DROP TABLE IF EXISTS `patientsrequest`;

CREATE TABLE `patientsrequest` (
  `Patient_Id` int(255) NOT NULL auto_increment,
  `Patient_name` varchar(255) default NULL,
  `Patient_Emailid` varchar(255) default NULL,
  `Date` varchar(255) default NULL,
  `Doctorname` varchar(255) default NULL,
  `BrainTumorimage` varchar(255) default NULL,
  `massage` longtext,
  `symptoms` varchar(255) default NULL,
  `userimage` varchar(255) default NULL,
  `disease` varchar(255) default 'NOT CHECK',
  PRIMARY KEY  (`Patient_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `patientsrequest` */

insert  into `patientsrequest`(`Patient_Id`,`Patient_name`,`Patient_Emailid`,`Date`,`Doctorname`,`BrainTumorimage`,`massage`,`symptoms`,`userimage`,`disease`) values (2,'kalpesh','sujay@gmail.com','2023-11-24','stawar','static/upload\\c2.jpg','vvvvvvvvvvvvvvvvvvvvvvvvvvvv','Fever,Shortness of breath,Loss of taste or smell','static/Users\\t1.jpg','The brain tumor is classified as meningioma tumor'),(3,'ketan','roshlyn2000@gmail.com','2023-12-12','stawar','static/upload\\p_2.jpg','please check and let me know','Fever,Cough,Shortness of breath','static/Users\\team1.jpg','The brain tumor is classified as meningioma tumor');

/*Table structure for table `userregisters` */

DROP TABLE IF EXISTS `userregisters`;

CREATE TABLE `userregisters` (
  `id` int(255) NOT NULL auto_increment,
  `Username` varchar(255) default NULL,
  `Email` varchar(255) default NULL,
  `Mobile` varchar(255) default NULL,
  `Password` varchar(255) default NULL,
  `Profile_Img` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `userregisters` */

insert  into `userregisters`(`id`,`Username`,`Email`,`Mobile`,`Password`,`Profile_Img`) values (1,'roshan','roshu@gmail.com','9561161391','a','static/Users\\t1.jpg'),(2,'ketan','roshlyn2000@gmail.com','9561161391','aa','static/Users\\team1.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
