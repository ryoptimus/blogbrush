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
    
def tag_amount_is_valid(tag_amount):
    if tag_amount == 'stringgg':
        return False
    if int(tag_amount) > 0 and int(tag_amount) < 5:
        return True
    print('Tag amount must be between 1 and 4.')
    return False
    
def tag_is_valid(tag):
    # Default tag, don't print anything
    if tag == 'mo,om':
        return False
    elif not tag:
        print('\tTag cannot be blank. Please try again.')
        return False
    elif ',' in tag:
        print('\tTag cannot contain commas. Please try again.')
        return False
    else: 
        return True
    
def datestring_is_valid(datestring):
    if not datestring:
        return False
    
    date_parts = datestring.split(' ')

    if len(date_parts) != 5:
        return False
    if int(date_parts[0]) > 2025 or int(date_parts[0]) < 2007:
        # Tumblr was founded in 2007. Year must be after that
        print('\tInvalid year. Year value must be between 2007 and 2025.')
        return False
    if int(date_parts[1]) < 1 or int(date_parts[1]) > 12:
        print('\tInvalid month. Month value must be between 1 and 12.')
        return False
    if int(date_parts[2]) < 1 or int(date_parts[2]) > 31:
        print('\tInvalid day. Day value must be between 1 and 31.')
        return False
    if int(date_parts[3]) < 0 or int(date_parts[3]) > 23:
        print('\tInvalid hour. Hour value must be between 0 and 23.')
        return False
    if int(date_parts[4]) < 0 or int(date_parts[4]) > 59:
        print('\tInvalid minute(s). Minute value must be between 0 and 59.')
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

    if len(date_parts[3]) == 1:
        date_parts[3] = '0' + date_parts[3]

    if len(date_parts[4]) == 1:
        date_parts[4] = '0' + date_parts[4]

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
    tags = None
    offset = None
    before = None
    after = None
    limit = None
    none = None

    if 'n' in qparams or 'none' in qparams:
        print('You have no query parameters to set. Cool.')
        none = True
    else:
        print('\nPlease provide values for your chosen query parameters.\n' \
              'If an invalid value is provided, you will be prompted to input the value again.\n')
        for qp in qparams:
            if qp == 't' or qp == 'type':
                type = 'subtweet'
                type_options = ['text', 'quote', 'link', 'answer', 'video', 'audio', 'photo', 'chat']
                while type not in type_options:
                    type = input('\tPost type (text, quote, link, answer, video, audio, photo, chat): ')
                print(f'\tYou have chosen {type} as your post type.\n')
            elif qp == 'h' or qp == 'hashtag':
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
                print(f"\tYou have selected the following tags: {', '.join(tags)}\n")
            elif qp == 'o' or qp == 'offset':
                while not offset.isdigit():
                    offset = input('\tOffset (post number to start at): ')
                print(f'\tYou have chosen {offset} as your offset.\n')
            elif qp == 'b' or qp == 'before':
                print('\tInput the desired date to search before.\n\t' \
                    'Date must be entered in year-month-date-hour-minute format separated by spaces.')
                while not datestring_is_valid(before):
                    before = input('\tYour entry: ')
                print(f'You have entered {datestring_to_readable_format(before)} as your desired search-before date.\n')
            elif qp == 'a' or qp == 'after':
                print('\tInput the desired date to search after.\n\t' \
                    'Date must be entered in year-month-date-hour-minute format separated by spaces.')
                while not datestring_is_valid(after):
                    after = input('\tYour entry: ')
                print(f'\tYou have entered {datestring_to_readable_format(after)} as your desired search-after date.\n')
            elif qp == 'l' or qp == 'limit':
                while not limit_is_valid(limit):
                    limit = input('\tInput limit of posts to alter / read (1-20): ')
                print(f'\tYou have entered {limit} as your desired limit.\n')

    return type, tags, offset, before, after, limit, none

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
    type, tags, offset, before, after, limit, none = parse_qparams(qparams)
    if not none:
        if type:
            request_url = request_url + f'/{type.lower()}'
        if tags:
            if '?' not in request_url:
                sep = '?'
            else:
                sep = '&'

            # Step 2: Build each tag parameter with its index
            tag_params = []
            for i, tag in enumerate(tags):
                tag_params.append(f'tag[{i}]={tag}')

            # Step 3: Join all tag parameters with &
            tag_query = '&'.join(tag_params)

            # Step 4: Append to the request URL
            request_url = request_url + sep + tag_query
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