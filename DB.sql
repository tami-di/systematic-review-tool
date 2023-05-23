SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `papers2` DEFAULT CHARACTER SET utf8 ;
USE `papers2` ;

DROP TABLE IF EXISTS papers2.paper;
CREATE TABLE papers2.paper (
  id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(200) NOT NULL,
  library varchar(20) DEFAULT NULL,
  code_name varchar(30) DEFAULT NULL,
  year year(4) DEFAULT NULL,
  abstract text,
  summary text,
  source varchar(30) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.author;
CREATE TABLE papers2.author (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(50) DEFAULT NULL,
  affiliation text,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.categories;
CREATE TABLE papers2.categories (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  description text,
  extra text,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.content;
CREATE TABLE papers2.content (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  description text,
  extra text,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.interaction;
CREATE TABLE papers2.interaction (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.paper_has_authors;
CREATE TABLE papers2.paper_has_authors (
  author_id mediumint(9) NOT NULL,
  paper_id int(11) NOT NULL,
  KEY author_id (author_id),
  KEY paper_n_id (paper_id),
  FOREIGN KEY (author_id) REFERENCES author (id),
  FOREIGN KEY (paper_id) REFERENCES paper (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.paper_has_cont;
CREATE TABLE papers2.paper_has_cont (
  paper_id int(11) NOT NULL,
  cat_id mediumint(9) NOT NULL,
  cont_id mediumint(9) NOT NULL,
  KEY paper_id (paper_id),
  KEY cat_id (cat_id),
  KEY cont_id (cont_id),
  FOREIGN KEY (paper_id) REFERENCES paper (id),
  FOREIGN KEY (cat_id) REFERENCES categories (id),
  FOREIGN KEY (cont_id) REFERENCES content (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.cat_cont;
CREATE TABLE papers2.cat_cont (
  cat_id mediumint(9) NOT NULL,
  cont_id mediumint(9) NOT NULL,
  KEY cat_id (cat_id),
  KEY cont_id (cont_id),
  FOREIGN KEY (cat_id) REFERENCES categories (id),
  FOREIGN KEY (cont_id) REFERENCES content (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.int_cat;
CREATE TABLE papers2.int_cat (
  cat_id1 mediumint(9) NOT NULL,
  int_id mediumint(9) NOT NULL,
  cat_id2 mediumint(9) NOT NULL,
  KEY cat_id1 (cat_id1),
  KEY int_id (int_id),
  KEY cat_id2 (cat_id2),
  FOREIGN KEY (cat_id1) REFERENCES categories (id),
  FOREIGN KEY (int_id) REFERENCES interaction (id),
  FOREIGN KEY (cat_id2) REFERENCES categories (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS papers2.int_cont;
CREATE TABLE papers2.int_cont (
  cont_id1 mediumint(9) NOT NULL,
  int_id mediumint(9) NOT NULL,
  cont_id2 mediumint(9) NOT NULL,
  KEY cont_id1 (cont_id1),
  KEY int_id (int_id),
  KEY cont_id2 (cont_id2),
  FOREIGN KEY (cont_id1) REFERENCES content (id),
  FOREIGN KEY (int_id) REFERENCES interaction (id),
  FOREIGN KEY (cont_id2) REFERENCES content (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
