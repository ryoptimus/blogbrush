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
               'l', 'likes',
               'd', 'drafts']

    while target.lower() not in targets:
        target = input('\nWTW?\n\t' \
        'For posts, type p or posts.\n\t' \
        'For likes, type l or likes.\n\t' \
        'For drafts, type d or drafts.\n\n\t' \
        'Selection: ')

    if target.lower() == 'p' or target.lower() == 'posts':
        print('You have selected posts.\n')
    elif target.lower() == 'l' or target.lower() == 'drafts':
        print('You have selected drafts.\n')
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
        # IDK what else you can do with drafts and idrc rn
        print('Default functionality for drafts is read. Hope you brought your spectacles.\n')
        return 'r'
    
    while function.lower() not in functions:
        function = input(prompt_string)
    
    if function.lower() == 'r' or function.lower == 'read':
        print('You have chosen the read function.\n')
    elif function.lower() == 'd' or function.lower == 'delete':
        print('You have chosen the delete function.\n')
    elif function.lower() == 'e' or function.lower == 'edit':
        print('You have chosen the edit function.\n')
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

    if target == 'p' or target == 'posts':
        input_prompt = '\nWhat query parameters would you like to specify?\n\t' \
        'Type (t, type): the type of post to return\n\t' \
        'Tag (h, hashtag): limits the response to posts with the specified tag(s)\n\t' \
        'Offset (o, offset): post number to start at (0 is the first post)\n\t' \
        'Before (b, before): returns posts published before a specified timestamp\n\t' \
        'After (a, after): returns posts published before a specified timestamp\n\t' \
        'Limit (l, limit): the number of results to return (1–20, inclusive)\n\t' \
        'None (n, none): indicates no selection\n\n\t' \
        'Your selection should be a string of characters separated by spaces.\n\t\t' \
        'e.g., o l OR offset limit to indicate you wish to specify offset and limit\n\n\t' \
        'Selection: '
    elif target == 'l' or target == 'likes':
        input_prompt = '\nWhat query parameters would you like to specify?\n\t' \
        'Offset (o, offset): post number to start at\n\t' \
        'Before (b, before): returns posts liked before a specified timestamp\n\t' \
        'After (a, after): returns posts liked before a specified timestamp\n\t' \
        'Limit (l, limit): the number of results to return (1–20, inclusive)\n\t' \
        'None (n, none): indicates no selection\n\n\t' \
        'Your selection should be a string of characters separated by spaces.\n\t\t' \
        'e.g., o l OR offset limit to indicate you wish to specify offset and limit\n\n\t' \
        'Selection: '
    # Drafts only support before_id and filter as query parameters but idc about those
    else:
        qparams = 'n'
        return qparams

    while not qparams_are_valid(qparams):
        qparams = input(input_prompt)
    
    qparams = list(qparams)
    return qparams

def get_type(session):
    type = 'subtweet'
    type_options = ['text', 'quote', 'link', 'answer', 'video', 'audio', 'photo', 'chat']
    while type not in type_options:
        type = input('\tPost type (text, quote, link, answer, video, audio, photo, chat): ')
    print(f'\tYou have chosen {type} as your post type.\n')
    session.set_type(type)

def get_tags(session):
    tag_amount = 'stringgg'
    print('\tHow many tags would you like to specify?')
    while not tag_amount_is_valid(tag_amount):
        tag_amount = input('\t\tAmount: ')
    tag_amount = int(tag_amount)
    print(f'\tYou have chosen to specify {tag_amount} tag(s). Input them below.')
    tags = []
    for i in range(tag_amount):
        tag = 'mo,om'
        while not tag_is_valid(tag):
            tag = input(f'\t\tTag {i + 1}: ')
        tag = format_tag(tag)
        tags.append(tag)
    print(f"\tYou have selected the following tag(s): {', '.join(tags)}\n")
    session.set_tags(tags)

def get_offset(session):
    offset = None
    while offset is None or not offset.isdigit():
        offset = input('\tOffset (post number to start at): ')
    print(f'\tYou have chosen {offset} as your offset.\n')
    session.set_offset(offset)

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

def get_searchdate(session, date_qp):
    if date_qp == 'b' or date_qp == 'before':
        before = None
        print('\tInput the desired date to search before.\n\t' \
                'Date must be entered in year-month-date-hour-minute format separated by spaces.')
        while not datestring_is_valid(before):
            before = input('\tYour entry: ')
        print(f'\tYou have entered {datestring_to_readable_format(before)} as your desired search-before date.\n')
        session.set_before(convert_to_unix_time(before))
    else:
        after = None
        print('\tInput the desired date to search after.\n\t' \
                'Date must be entered in year-month-date-hour-minute format separated by spaces.')
        while not datestring_is_valid(after):
            after = input('\tYour entry: ')
        print(f'\tYou have entered {datestring_to_readable_format(after)} as your desired search-after date.\n')
        session.set_after(convert_to_unix_time(after))
    
def get_limit(session):
    limit = None
    while not limit_is_valid(limit):
        limit = input('\tInput limit of posts to alter / read (1-20): ')
    print(f'\tYou have entered {limit} as your desired limit.\n')
    session.set_limit(int(limit))

def parse_qparams(session, qparams):
    none = None

    if 'n' in qparams or 'none' in qparams:
        print('You have no query parameters to set. Cool.\n')
        none = True
    else:
        print('\nPlease provide values for your chosen query parameters.\n' \
              'If an invalid value is provided, you will be prompted to input the value again.\n')
        for qp in qparams:
            if qp == 't' or qp == 'type':
                get_type(session)
            elif qp == 'h' or qp == 'hashtag':
                get_tags(session)
            elif qp == 'o' or qp == 'offset':
                get_offset(session)
            elif qp == 'b' or qp == 'before':
                get_searchdate(session, qp)
            elif qp == 'a' or qp == 'after':
                get_searchdate(session, qp)
            elif qp == 'l' or qp == 'limit':
                get_limit(session)

    return none

def append_type_to_url(session):
    request_url = session.request_url
    type = session.get_param('type')
    request_url += f'/{type.lower()}'
    session.request_url = request_url

def append_tags_to_url(session):
    request_url = session.request_url
    tags = session.get_param('tags')
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
    session.request_url = request_url

def append_param_to_url(session, param_name):
    request_url = session.request_url
    param = session.get_param(param_name)

    if '?' in request_url:
        request_url += f'&{param_name}={param}'
    else:
        request_url += f'?{param_name}={param}'

    session.request_url = request_url

def append_qparams_to_url(session, qparams):
    none = parse_qparams(session, qparams)
    if not none:
        type = session.get_param('type')
        if type:
            append_type_to_url(session)
        tags = session.get_param('tags')
        if tags:
            append_tags_to_url(session)
        offset = session.get_param('offset')
        if offset:
            append_param_to_url(session, 'offset')
        before = session.get_param('before')
        if before:
            append_param_to_url(session, 'before')
        after = session.get_param('after')
        if after:
            append_param_to_url(session, 'after')
        limit = session.get_param('limit')
        if limit:
            append_param_to_url(session, 'limit')