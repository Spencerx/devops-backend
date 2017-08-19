/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 5.6.17 : Database - devops
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`devops` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `devops`;

/*Table structure for table `services` */

DROP TABLE IF EXISTS `services`;

CREATE TABLE `services` (
  `s_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(256) NOT NULL,
  `war_url` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

/*Data for the table `services` */

insert  into `services`(`s_id`,`service_name`,`war_url`) values (1,'haixue_appExternal ',NULL),(2,'haixue_crmx',NULL),(3,'haixue_order',NULL),(4,'haixue_cmonitor2',NULL),(5,'haixue_crmxtask',NULL),(6,'haixue_question',NULL),(7,'haixue_course',NULL),(8,'haixue_end',NULL),(9,'haixue_static',NULL),(10,'haixue_crm_label_collector_consumer',NULL),(11,'haixue_exam',NULL),(12,'haixue_workshop',NULL),(13,'haixue_crmorder',NULL),(14,'haixue_external',NULL),(15,'haixue_www',NULL),(16,'haixue_crm_order_mq_consumer',NULL);

/*Table structure for table `teams` */

DROP TABLE IF EXISTS `teams`;

CREATE TABLE `teams` (
  `t_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_name` varchar(128) NOT NULL,
  PRIMARY KEY (`t_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `teams` */

insert  into `teams`(`t_id`,`team_name`) values (1,'app'),(2,'website'),(3,'ops'),(4,'product');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

/*Data for the table `users` */

insert  into `users`(`id`,`username`,`password`) values (34,'1','pbkdf2:sha256:50000$FKKh6ikJ$25b7da3474a7fb8ce6511121551dc3f3c224ee2b5c8edc51d11fa9b448802be1'),(35,'admin','pbkdf2:sha256:50000$XnkbawBJ$886831653e67c9987fb8ae357b00474f14df3ed94ff3af3b25b8c85abebda3ff');

/*Table structure for table `workflow` */

DROP TABLE IF EXISTS `workflow`;

CREATE TABLE `workflow` (
  `service` varchar(256) NOT NULL,
  `w_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_name` varchar(128) NOT NULL,
  `dev_user` varchar(128) NOT NULL,
  `test_user` varchar(128) NOT NULL,
  `production_user` varchar(128) NOT NULL,
  `sql_info` varchar(2048) DEFAULT NULL,
  `jenkins_version` varchar(1024) DEFAULT NULL,
  `v_version` varchar(1024) DEFAULT NULL,
  `last_jenkins_version` varchar(1024) DEFAULT NULL,
  `comment` varchar(2048) DEFAULT NULL,
  `deploy_info` varchar(4068) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`w_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Data for the table `workflow` */

insert  into `workflow`(`service`,`w_id`,`team_name`,`dev_user`,`test_user`,`production_user`,`sql_info`,`jenkins_version`,`v_version`,`last_jenkins_version`,`comment`,`deploy_info`,`create_time`) values ('',1,'mobile','sql','test_sql','pro_sql','insert','1.0','1.2','0.8','haha','info more','2017-08-17 16:58:16'),('',2,'web','1','2','3','4','5','6','7','8','9','2017-08-16 16:58:42'),('haixue_crmx',3,'website','sql ','cjz','yy','select;insert','10',NULL,'9','nonono','nonono','2017-08-18 22:45:20'),('haixue_crmx',4,'website','s','s','s','','s',NULL,'s','s','s','2017-08-18 22:49:08'),('haixue_crmx',5,'website','a','s','s','','s',NULL,'s','s','s','2017-08-18 22:49:35'),('haixue_crmx',6,'website','s','s','s','s','s',NULL,'s','s','s','2017-08-18 22:53:37'),('haixue_crmx',7,'ops','s','s','s','','s',NULL,'s','s','s','2017-08-18 22:54:23');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
