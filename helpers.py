import re
import json
import datetime

from validator import (
    qparams_are_valid, tag_amount_is_valid, tag_is_valid, datestring_is_valid, limit_is_valid
)

def get_blog_name():
    confirm_blog = False
    while not confirm_blog:
        # Get blog name from user
        blog_name = input('Enter blog name: ')

        confirm_blog_name = input(f'You have entered {blog_name}. Please confirm (y/n): ')
    
        if confirm_blog_name.lower() == 'y':
            confirm_blog = True

    if blog_name.endswith('.tumblr.com'):
        blog_name = blog_name.split('.')[0]

    return blog_name

def craft_blog_id(blog_name):
    return blog_name + '.tumblr.com'

def get_target():
    target = 'x'
    targets = ['p', 'posts',
               'q', 'qposts',
               'l', 'likes',
               'd', 'drafts']

    while target.lower() not in targets:
        target = input('\nWTW?\n\t' \
        'For posts, type p or posts.\n\t' \
        'For queued posts, type q or qposts.\n\t' \
        'For likes, type l or likes.\n\t' \
        'For drafts, type d or drafts.\n\n\t' \
        'Selection: ')

    if target.lower() == 'p' or target.lower() == 'posts':
        print('You have selected posts.\n')
    elif target.lower() == 'q' or target.lower() == 'qposts':
        print('You have selected queued posts.\n')
    elif target.lower() == 'l' or target.lower() == 'likes':
        print('You have selected likes.\n')
    else:
        print('You have selected drafts.\n')

    return target

def get_function(target):
    function = 'x'
    if target == 'p' or target == 'posts':
        functions = ['r', 'read',
                    'd', 'delete',
                    'e', 'edit']
        prompt_string = 'What do you want to do with these posts?\n\t' \
        'For reading, type r or read.\n\tFor deleting, type d or delete.\n\t' \
        'For editing, type e or edit.\n\n\tSelection: '
    elif target == 'l' or target == 'likes':
        functions = ['r', 'read',
                     'u', 'unlike']
        prompt_string = 'What do you want to do with these posts?\n\t' \
        'For reading, type r or read.\n\tFor unliking, type u or unlike.\n\n\t' \
        'Selection: '
    else:
        # IDK what else you can do with queued posts/drafts and idrc rn
        print('Default functionality for queued posts and drafts is read. Hope you brought your spectacles.\n')
        return 'r'
    
    while function.lower() not in functions:
        function = input(prompt_string)
    
    if function.lower() == 'r' or function.lower == 'read':
        print('You have chosen the read function.\n')
    elif function.lower() == 'd' or function.lower == 'delete':
        print('You have chosen the delete function.\n')
    else:
        print('You have chosen the edit function.\n')

    return function

def datestring_to_readable_format(datestring):
    datestring_formatted = ''
    date_parts = datestring.split(' ')

    if int(date_parts[1]) == 1:
        month = 'January'
    elif int(date_parts[1]) == 2:
        month = 'February'
    elif int(date_parts[1]) == 3:
        month = 'March'
    elif int(date_parts[1]) == 4:
        month = 'April'
    elif int(date_parts[1]) == 5:
        month = 'May'
    elif int(date_parts[1]) == 6:
        month = 'June'
    elif int(date_parts[1]) == 7:
        month = 'July'
    elif int(date_parts[1]) == 8:
        month = 'August'
    elif int(date_parts[1]) == 9:
        month = 'September'
    elif int(date_parts[1]) == 10:
        month = 'October'
    elif int(date_parts[1]) == 11:
        month = 'November'
    else:
        month = 'December'

    if len(date_parts[3]) == 1:
        date_parts[3] = '0' + date_parts[3]

    if len(date_parts[4]) == 1:
        date_parts[4] = '0' + date_parts[4]

    datestring_formatted += f'{date_parts[3]}:{date_parts[4]} {date_parts[2]} {month} {date_parts[0]}'

    return datestring_formatted

def format_tag(tag):
    formatted_tag = tag.replace(' ', '+')
    return formatted_tag

def get_qparams(target):
    qparams = 'x x x x'

    if target.lower() == 'p' or target.lower() == 'posts':
        input_prompt = '\nWhat query parameters would you like to specify?\n\t' \
        'Type (t, type): the type of post to return\n\t' \
        'Tag (h, hashtag): limits the response to posts with the specified tag(s)\n\t' \
        'Offset (o, offset): post number to start at (0 is the first post)\n\t' \
        'Before (b, before): returns posts published before a specified timestamp\n\t' \
        'After (a, after): returns posts published before a specified timestamp\n\t' \
        'Limit (l, limit): the number of results to return (1–260, inclusive)\n\t' \
        'None (n, none): indicates no selection\n\n\t' \
        'Your selection should be a string of characters separated by spaces.\n\t\t' \
        'e.g., \'o l\' OR \'offset limit\' to indicate you wish to specify offset and limit\n\n\t' \
        'Selection: '
    elif target.lower() == 'q' or target.lower() == 'qposts':
        input_prompt = '\nWhat query parameter would you like to specify?\n\t' \
        'Offset (o, offset): post number to start at (0 is the first post)\n\t' \
        'Limit (l, limit): the number of results to return (1–260, inclusive)\n\t' \
        'None (n, none): indicates no selection\n\n\t' \
        'e.g., \'o l\' OR \'offset limit\' to indicate you wish to specify offset and limit\n\n\t' \
        'Selection: '
    elif target.lower() == 'l' or target.lower() == 'likes':
        input_prompt = '\nWhat query parameters would you like to specify?\n\t' \
        'Offset (o, offset): post number to start at (1,000 max)\n\t' \
        'Before (b, before): returns posts liked before a specified timestamp\n\t' \
        'After (a, after): returns posts liked before a specified timestamp\n\t' \
        'Limit (l, limit): the number of results to return (1–260, inclusive)\n\t' \
        'None (n, none): indicates no selection\n\n\t' \
        'Your selection should be a string of characters separated by spaces.\n\t\t' \
        'e.g., \'o l\' OR \'offset limit\' to indicate you wish to specify offset and limit\n\n\t' \
        'Selection: '
    # Drafts only support before_id and filter as query parameters but idc about those
    else:
        qparams = 'n'
        return qparams

    while not qparams_are_valid(qparams):
        qparams = input(input_prompt)
    
    qparams = list(qparams)
    return qparams

def get_type(instance):
    type = 'subtweet'
    type_options = ['text', 'quote', 'link', 'answer', 'video', 'audio', 'photo', 'chat']
    while type not in type_options:
        type = input('\tPost type (text, quote, link, answer, video, audio, photo, chat): ')
    print(f'\tYou have chosen {type} as your post type.\n')
    instance.set_type(type)

def get_tags(instance):
    tag_amount = None
    print('\tHow many tags would you like to specify?')
    while not tag_amount_is_valid(tag_amount):
        tag_amount = input('\t\tAmount: ')
    tag_amount = int(tag_amount)
    print(f'\tYou have chosen to specify {tag_amount} tag(s). Input them below.')
    tags = []
    for i in range(tag_amount):
        tag = None
        while not tag_is_valid(tag):
            tag = input(f'\t\tTag {i + 1}: ')
        tag = format_tag(tag)
        tags.append(tag)
    print(f'\tYou have selected the following tag(s): {', '.join(tags)}\n')
    instance.set_tags(tags)

def get_offset(instance):
    offset = None
    while offset is None or not offset.isdigit():
        offset = input('\tOffset (post number to start at): ')
    print(f'\tYou have chosen {offset} as your offset.\n')
    instance.set_offset(offset)

def convert_to_unix_time(datestring):
    if not datestring:
        return False
    
    date_parts = datestring.split(' ')
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    hours = int(date_parts[3])
    minutes = int(date_parts[4])

    dt = datetime.datetime(year, month, day, hours, minutes)
    res = dt.timestamp()
    return int(res)

def get_searchdate(instance, date_qp):
    if date_qp == 'b' or date_qp == 'before':
        before = None
        print('\tInput the desired date to search before.\n\t' \
                'Date must be entered in year-month-date-hour-minute format separated by spaces.')
        while not datestring_is_valid(before):
            before = input('\tYour entry: ')
        print(f'\tYou have entered {datestring_to_readable_format(before)} as your desired search-before date.\n')
        instance.set_before(convert_to_unix_time(before))
    else:
        after = None
        print('\tInput the desired date to search after.\n\t' \
                'Date must be entered in year-month-date-hour-minute format separated by spaces.')
        while not datestring_is_valid(after):
            after = input('\tYour entry: ')
        print(f'\tYou have entered {datestring_to_readable_format(after)} as your desired search-after date.\n')
        instance.set_after(convert_to_unix_time(after))
    
def get_limit(instance):
    limit = None
    while not limit_is_valid(limit):
        limit = input('\tInput limit of posts to alter / read (1-260): ')
    print(f'\tYou have entered {limit} as your desired limit.\n')
    instance.set_limit(int(limit))

def parse_qparams(instance, qparams):
    none = None

    if 'n' in qparams or 'none' in qparams:
        print('You have no query parameters to set. Cool.\n')
        none = True
    else:
        print('\nPlease provide values for your chosen query parameters.\n' \
              'If an invalid value is provided, you will be prompted to input the value again.\n')
        for qp in qparams:
            if qp == 't' or qp == 'type':
                get_type(instance)
            elif qp == 'h' or qp == 'hashtag':
                get_tags(instance)
            elif qp == 'o' or qp == 'offset':
                get_offset(instance)
            elif qp == 'b' or qp == 'before':
                get_searchdate(instance, qp)
            elif qp == 'a' or qp == 'after':
                get_searchdate(instance, qp)
            elif qp == 'l' or qp == 'limit':
                get_limit(instance)

    return none

def append_type_to_url(instance, type):
    # Also only works if the type has not been added yet
    request_url = instance.request_url
    request_url += f'/{type.lower()}'
    instance.request_url = request_url

def append_tags_to_url(instance, tags):
    # This one only works if the tags have not been added yet
    request_url = instance.request_url

    if '?' not in request_url:
        sep = '?'
    else:
        sep = '&'

    # Build each tag parameter with its index
    tag_params = []
    for i, tag in enumerate(tags):
        tag_params.append(f'tag[{i}]={tag}')

    # Join all tag parameters with &
    tag_query = '&'.join(tag_params)

    # Append to the request URL
    request_url = request_url + sep + tag_query
    instance.request_url = request_url

def append_param_to_url(instance, param_name, param):
    request_url = instance.request_url
    if param_name == 'limit' and param > 20:
        return
    if f'{param_name}=' in request_url:
        base, query = request_url.split('?', 1)
        parts = query.split('&')

        for i, p in enumerate(parts):
            if p.startswith(f'{param_name}='):
                parts[i] = f'{param_name}={param}'
                break

        request_url = base + '?' + '&'.join(parts)
    else:
        if '?' in request_url:
            request_url += f'&{param_name}={param}'
        else:
            request_url += f'?{param_name}={param}'

    instance.request_url = request_url

def append_qparams_to_url(instance, qparams):
    none = parse_qparams(instance, qparams)
    if not none:
        type = instance.get_param('type')
        if type:
            append_type_to_url(instance, type)
        tags = instance.get_param('tags')
        if tags:
            append_tags_to_url(instance, tags)
        offset = instance.get_param('offset')
        if offset:
            append_param_to_url(instance, 'offset', offset)
        before = instance.get_param('before')
        if before:
            append_param_to_url(instance, 'before', before)
        after = instance.get_param('after')
        if after:
            append_param_to_url(instance, 'after', after)
        limit = instance.get_param('limit')
        if limit:
            append_param_to_url(instance, 'limit', limit)

def get_edit_info():
    valid_fxn = False
    while not valid_fxn:
        function_query = '\tDo you want to delete (d, delete) or add (a, add) a tag?\n\t\tYour entry: '
        function = input(function_query)
        if function == 'a' or function == 'add':
            valid_fxn = True
        if function == 'd' or function == 'delete':
            valid_fxn = True
    if function == 'd' or function == 'delete':
        tag_query = '\tInput the tag you wish to delete: '
    else:
        tag_query = '\tInput the tag you wish to add: '
    valid_tag = False
    while not valid_tag:
        tag = input(tag_query)
        if not ',' in tag:
            valid_tag = True
    return function, tag

def edit_tags_list(function, tags, tag):
    if function == 'd' or function == 'delete':
        if tag not in tags:
            print(f'F@#&! Looks like this post doesn\'t contain tag \'{tag}.\' No editing to be done here...')
            return tags
        tags.remove(tag)
        return tags
    else:
        tags.append(tag)
        return tags
    
def pretty_print_response(resp):
    print(f'Status: {resp.status_code}')
    try:
        print(json.dumps(resp.json(), indent=4))
    except ValueError:
        print(resp.text)