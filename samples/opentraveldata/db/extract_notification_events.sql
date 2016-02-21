
--
-- Foreign key on the trackers table
--
select ne.timestamp as ts, ne.tag_list as tl,
	   tck.check_frequency as cf, tck.thshd_lower as tl, tck.thshd_upper as tu,
	   tck.notification_list as nl, ne.content as ct
from sdq_sdq.trackers as tck,
	 sdq_sdq.notification_events as ne
where ne.tag_list = tck.tag_list;
