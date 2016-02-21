
--
-- Table structure to manage the trackers
--
drop table if exists `trackers`;
create table `trackers` (
  `tag_list` text not null,
  `check_frequency` int(6) default 60,
  `thshd_lower` decimal(5,2) default 0.75,
  `thshd_upper` decimal(5,2) default 1.5,
  `notification_list` text default null
) charset=utf8;

--
-- Table structure to manage the notification events
--
drop table if exists `notification_events`;
create table `notification_events` (
  `timestamp` timestamp not null,
  `tag_list` text not null,
  `content` text default null
) charset=utf8;
