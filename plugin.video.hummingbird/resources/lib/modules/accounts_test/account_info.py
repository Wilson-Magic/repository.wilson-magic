account_sort = {
    'kitsu': {
        'Update Date': '-progressed_at',
        '-Update Date': 'progressed_at',
        'Progress': '-progress',
        '-Progress': 'progress',
        'Alphabetical': 'anime.titles.canonical'
        },
    'mal': {
        'Update Date': 'order=5&status=%s',
        '-Update Date': 'order=5&status=%s',
        'Progress': 'order=12&status=%s',
        '-Progress': 'order=12&status=%s',
        'Alphabetical': 'order=1&status=%s'
        },
    'anilist': {
        'Update Date': 'UPDATED_TIME',
        '-Update Date': 'UPDATED_TIME',
        'Progress': 'PROGRESS',
        '-Progress': 'PROGRESS',
        'Alphabetical': 'UPDATED_TIME'
        }
    }
    
def map_to_item(progress_list, item_list):
    mapped_items = []

    index = 0
    for a in progress_list:
        new_dict = item_list[index]
        new_dict['account_info'] = {
            'status': a['attributes']['status'],
            'progress': a['attributes']['progress']
            }
        mapped_items.append(new_dict)
        index += 1
        
    return mapped_items