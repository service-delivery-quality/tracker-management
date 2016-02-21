
--
-- Foreign key on the trackers table
--
select ne.timestamp, ne.tag_list,
	   tck.check_frequency, tck.thshd_lower, tck.thshd_upper,
	   tck.notification_list, ne.content
from sdq_sdq.trackers as tck,
	 sdq_sdq.notification_events as ne
where ne.tag_list = tck.tag_list;
