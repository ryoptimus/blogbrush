import datetime

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

    return target

def get_function(target):
    function = 'x'
    if target == 'p' or target == 'posts':
        functions = ['r', 'read',
                    'd', 'delete',
                    'e', 'edit']
        prompt_string = '\nWhat do you want to do with these posts?\n\t' \
        'For reading, type r or read.\n\tFor deleting, type d or delete.\n\t' \
        'For editing, type e or edit.\n\n\tSelection: '
    elif target == 'l' or target == 'likes':
        functions = ['r', 'read',
                     'u', 'unlike']
        prompt_string = '\nWhat do you want to do with these posts?\n\t' \
        'For reading, type r or read.\n\tFor unliking, type u or unlike.\n\n\t' \
        'Selection: '
    else:
        # IDK what else you can do with drafts and idrc rn
        return 'r'
    
    while function.lower() not in functions:
        function = input(prompt_string)
    
    return function

def qparams_are_valid(qparams_chosen):
    # Default case
    if qparams_chosen == 'x x x x':
        return False
    
    qparam_options = ['t', 'type', 'h', 'hashtag',
                      'o', 'offset', 'b', 'before',
                      'a', 'after', 'l', 'limit',
                      'n', 'none']
    
    # Convert qparams_chosen into list
    qparams_list = qparams_chosen.split(' ')

    # Remove duplicates (if applicable) while preserving order
    qparams = list(dict.fromkeys(qparams_list))

    if set(qparams).issubset(set(qparam_options)):
        if ('n' in qparams or 'none' in qparams) and len(qparams) > 1:
            print('If you include n or none in your response ' \
            'to indicate you wish to select no query parameters, ' \
            'that must be the only query parameter present.\nPlease try again.')
            return False
        if ('b' in qparams or 'before' in qparams) and ('o' in qparams or 'offset' in qparams):
            print('You cannot use before and offset in the same request.\nPlease try again.')
            return False
        print('\nGood. These are valid query parameters.')
        return True
    else:
        print('Error: Invalid parameters detected.\nPlease try again.')
        return False
    
def tag_is_valid(tag):
    if not tag:
        print('Tag cannot be blank. Please try again.')
        return False
    elif ',' in tag:
        print('Tag cannot contain commas. Please try again.')
        return False
    else: 
        return True
    
def datestring_is_valid(datestring):
    if not datestring:
        return False
    
    date_parts = datestring.split(' ')

    if len(date_parts) != 5:
        return False
    if int(date_parts[0]) > 2025 or int(date_parts[0]) < 1970:
        print('Invalid year. Year value must be between 1970 and 2025.')
        return False
    if int(date_parts[1]) < 1 or int(date_parts[1]) > 12:
        print('Invalid month. Month value must be between 1 and 12.')
        return False
    if int(date_parts[2]) < 1 or int(date_parts[2]) > 31:
        print('Invalid day. Day value must be between 1 and 31.')
        return False
    if int(date_parts[3]) < 0 or int(date_parts[3]) > 23:
        print('Invalid hour. Hour value must be between 0 and 23.')
        return False
    if int(date_parts[4]) < 0 or int(date_parts[4]) > 59:
        print('Invalid minute(s). Minute value must be between 0 and 59.')
        return False
    return True

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

    datestring_formatted += f'{date_parts[3]}:{date_parts[4]} {date_parts[2]} {month} {date_parts[0]}'

    return datestring_formatted

def limit_is_valid(limit):
    if not limit:
        return False
    if not limit.isdigit():
        return False
    limit_int = int(limit)
    if limit_int < 1 or limit_int > 20:
        return False
    return True

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

def parse_qparams(qparams):
    type = None
    tag = None
    offset = None
    before = None
    after = None
    limit = None
    none = None

    if not ('n' in qparams or 'none' in qparams):
        print('\nPlease provide values for your chosen query parameters.\n' \
              'If an invalid value is provided, you will be prompted to input the value again.\n')
    for qp in qparams:
        if qp == 't' or qp == 'type':
            type = 'subtweet'
            type_options = ['text', 'quote', 'link', 'answer', 'video', 'audio', 'photo', 'chat']
            while type not in type_options:
                type = input('\tPost type (text, quote, link, answer, video, audio, photo, chat): ')
            print(f'You have chosen {type} as your post type.')
        elif qp == 'h' or qp == 'hashtag':
            while not tag_is_valid(tag):
                tag = input('\tInput a valid tag. The tag may not include commas. ')
            print(f'You have chosen {tag} as a tag for filtering.')
            tag = format_tag(tag)
        elif qp == 'o' or qp == 'offset':
            while not offset.isdigit():
                offset = input('\tOffset (post number to start at): ')
            print(f'You have chosen {offset} as your offset.')
        elif qp == 'b' or qp == 'before':
            while not datestring_is_valid(before):
                before = input('\tInput the desired date to search before.\n\t' \
                'Date must be entered in year-month-date-hour-minute format separated by spaces.\n\tYour entry: ')
            print(f'You have entered {datestring_to_readable_format(before)} as your desired search-before date.')
        elif qp == 'a' or qp == 'after':
            while not datestring_is_valid(after):
                after = input('\tInput the desired date to search after.\n' \
                'Date must be entered in year-month-date-hour-minute format separated by spaces.\nYour entry: ')
            print(f'You have entered {datestring_to_readable_format(after)} as your desired search-after date.')
        elif qp == 'l' or qp == 'limit':
            while not limit_is_valid(limit):
                limit = input('\tInput limit of posts to alter / read (1-20): ')
            print(f'You have entered {limit} as your desired limit.')
        else:
            print('You have no query parameters to set. Cool.')
            none = True

    return type, tag, offset, before, after, limit, none

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

def append_qparams_to_url(request_url, qparams):
    type, tag, offset, before, after, limit, none = parse_qparams(qparams)
    if not none:
        if type:
            request_url = request_url + f'/{type.lower()}'
        if tag:
            if '?' in request_url:
                request_url = request_url + f'&tag={tag}'
            else:
                request_url = request_url + f'?tag={tag}'
        if offset:
            if '?' in request_url:
                request_url = request_url + f'&offset={offset}'
            else:
                request_url = request_url + f'?offset={offset}'
        if before:
            before_unix = convert_to_unix_time(before)
            if '?' in request_url:
                request_url = request_url + f'&before={before_unix}'
            else:
                request_url = request_url + f'?before={before_unix}'
        if after:
            after_unix = convert_to_unix_time(after)
            if '?' in request_url:
                request_url = request_url + f'&after={after_unix}'
            else:
                request_url = request_url + f'?after={after_unix}'
        if limit:
            if '?' in request_url:
                request_url = request_url + f'&limit={limit}'
            else:
                request_url = request_url + f'?limit={limit}'

    return request_url