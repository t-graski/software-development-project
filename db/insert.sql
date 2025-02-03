
-- INSERT DATA

INSERT INTO `departments` (`department_name`) VALUES
('Engineering'),
('Product'),
('Design'),
('Marketing'),
('Sales');

INSERT INTO `teams` (`team_name`, `department_id`) VALUES
('Engineering', 1),
('Product', 2),
('Design', 3),
('Marketing', 4),
('Sales', 5);

INSERT INTO `employees` (`firstname`, `lastname`, `email`, `password`, `role_tag`, `team_id`) VALUES
('John', 'Doe', 'john.doe@sky.net', 'password', 'admin', 1),
('Jane', 'Doe', 'jane.doe@sky.net', 'password', 'user', 1);

INSERT INTO `employee_teams` (`employee_id`, `team_id`) VALUES
(1, 1),
(2, 1);

INSERT INTO `health_check_types` (`type_id`, `display_name`) VALUES
('1', 'Health Check 1'),
('2', 'Health Check 2'),
('3', 'Health Check 3');

INSERT INTO `health_checks` (`employee_id`, `team_id`, `timestamp`) VALUES
(1, 1, NOW()),
(2, 1, NOW());

INSERT INTO `health_check_votes` (`check_id`, `type_id`, `vote`, `direction`) VALUES
(1, '1', 'green', 'up'),
(1, '2', 'red', 'down'),
(1, '3', 'amber', 'up'),
(2, '1', 'amber', 'up'),
(2, '2', 'green', 'up'),
(2, '3', 'red', 'up');