-- DROP TABLES
DROP TABLE IF EXISTS `health_check_votes`;
DROP TABLE IF EXISTS `health_checks`;
DROP TABLE IF EXISTS `health_check_types`;
DROP TABLE IF EXISTS `employee_teams`;
DROP TABLE IF EXISTS `employees`;
DROP TABLE IF EXISTS `teams`;
DROP TABLE IF EXISTS `departments`;

-- CREATE TABLES
CREATE TABLE `departments` (
    `department_id` INT(11) NOT NULL,
    `department_name` VARCHAR(50) NOT NULL,

    PRIMARY KEY (`department_id`)
);

CREATE TABLE `teams` (
    `team_id` INT(11) NOT NULL,
    `team_name` VARCHAR(50) NOT NULL,
    `department_id` INT(11) NOT NULL,

    PRIMARY KEY (`team_id`)
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE `employees` (
    `employee_id` INT(11) NOT NULL,
    `firstname` VARCHAR(50) NOT NULL,
    `lastname` VARCHAR(50) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `password` VARCHAR(50) NOT NULL,
    `role_tag` VARCHAR(50) NOT NULL,
    `team_id` INT(11) NOT NULL,

    PRIMARY KEY (`employee_id`)
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`team_id`)
);

CREATE TABLE `employee_teams` (
    `employee_id` INT(11) NOT NULL,
    `team_id` INT(11) NOT NULL,

    PRIMARY KEY (`employee_id`, `team_id`)
    FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`)
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`team_id`)
);

CREATE TABLE `health_check_types` (
    `type_id` VARCHAR(50) NOT NULL,
    `display_name` VARCHAR(50) NOT NULL,

    PRIMARY KEY (`type_id`)
);

CREATE TABLE `health_checks` (
    `check_id` INT(11) NOT NULL,
    `employee_id` INT(11) NOT NULL,
    `team_id` INT(11) NOT NULL,
    `timestamp` TIMESTAMP NOT NULL,

    PRIMARY KEY (`check_id`)
    FOREIGN KEY (`employee_id`, `team_id`) REFERENCES `employee_teams`(`employee_id`, `team_id`)
);

CREATE TABLE `health_check_votes` (
    `check_id` INT(11) NOT NULL,
    `type_id` VARCHAR(50) NOT NULL,
    `vote` VARCHAR(50) NOT NULL,
    `direction` VARCHAR(50) NOT NULL,

    PRIMARY KEY (`check_id`, `type_id`)
    FOREIGN KEY (`check_id`) REFERENCES `health_checks`(`check_id`)
    FOREIGN KEY (`type_id`) REFERENCES `health_check_types`(`type_id`)
);
