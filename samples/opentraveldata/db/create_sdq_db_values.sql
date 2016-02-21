
--
-- Table trackers
--
insert into `trackers` (`tag_list`, `check_frequency`,
	   				    `thshd_lower`, `thshd_upper`, `notification_list`)
values
('"file", "opentraveldata", "optd_airline_por.csv"', 1440, 0.7, 1.2, 'john@doe.me'),
('\"file\", \"opentraveldata\", \"optd_airlines.csv\"', 1440, 0.7, 1.2, 'john@doe.me')
;

--
-- Table notification_events
--
insert into `notification_events` (`timestamp`, `tag_list`, `content`)
values
('2016-02-01 08:00:00', '"file", "opentraveldata", "optd_airline_por.csv"', '{"notified_address_list": "john@doe.me"}'),
('2016-02-01 09:00:00', '"file", "opentraveldata", "optd_airlines.csv"', '{"notified_address_list": "john@doe.me"}')
;
