import json

with open("debug.html") as fi:
    content = fi.read()
    data = json.loads(eval(content))
    user = data['entry_data']['ProfilePage'][0]['graphql']['user']
    user_name = user['username']
    for edge in user['edge_owner_to_timeline_media']['edges']:
        #print(edge.keys())
        node = edge['node']
        display_url = node['display_url']
        is_video = node['is_video']
        taken_at = node['taken_at_timestamp']
        dim = node['dimensions']
        ch = dim['height']
        cw = dim['width']
        id = node['id']
        item = {
            'username': user_name,
            'image_url': display_url,
            'is_video': is_video,
            'taken_at': taken_at,
            'ch': ch,
            'cw': cw,
            'id': id
        }
        print(item)