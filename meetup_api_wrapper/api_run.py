import config
import wrapper

key = config.key
group_name = config.group_name

api = wrapper.meetupAPI(key)
data = api.get_group_members(group_name)
import pdb; pdb.set_trace()
