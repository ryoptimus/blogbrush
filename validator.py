# Helpers for validating user-provided query parameter inputs
from datetime import datetime

# TODO: Fix this for more robust checking
def valid_blogname(blogname):
    if len(blogname) > 32:
        print('Invalid input.')
        return False
    if blogname.contains(' '):
        print('Invalid input.')
        return False
    return True

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
    if tag_amount == None:
        return False
    if int(tag_amount) > 0 and int(tag_amount) < 5:
        return True
    print('Tag amount must be between 1 and 4.')
    return False
    
def tag_is_valid(tag):
    if tag == None:
        return False
    elif not tag:
        print('\t\tTag cannot be blank. Please try again.')
        return False
    elif ',' in tag:
        print('\t\tTag cannot contain commas. Please try again.')
        return False
    else: 
        return True
    
def datestring_is_valid(datestring):
    if not datestring:
        return False
    
    date_parts = datestring.split(' ')

    if len(date_parts) != 5:
        print('\tInvalid input. Date must be entered in year-month-date-hour-minute format separated by spaces.')
        return False

    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    hour = int(date_parts[3])
    minute = int(date_parts[4])

    current_year = datetime.now().year

    if year > current_year or year < 2007:
        # Tumblr was founded in 2007. Year must be after that
        print('\tInvalid year. Year value must be between 2007 and 2025.')
        return False
    if month < 1 or month > 12:
        print('\tInvalid month. Month value must be between 1 and 12.')
        return False
    if day < 1:
        print('\tInvalid day. Day value must be greater than 1.')
        return False
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if day > 31:
            print('\tInvalid day. Day value must not exceed 31.')
            return False
    if month in [4, 6, 9, 11]:
        if day > 30:
            print('\tInvalid day. Day value must not exceed 30.')
            return False
    if month == 2:
        if year % 4 == 0 and year % 100 != 0:
            if day > 29:
                print('\tInvalid day. Day value must not exceed 29.')
                return False
        else:
            if day > 28:
                print('\tInvalid day. Day value must not exceed 28.')
                return False
    if hour < 0 or hour > 23:
        print('\tInvalid hour. Hour value must be between 0 and 23.')
        return False
    if minute < 0 or minute > 59:
        print('\tInvalid minute(s). Minute value must be between 0 and 59.')
        return False
    return True

def limit_is_valid(limit):
    if not limit:
        return False
    if not limit.isdigit():
        return False
    limit_int = int(limit)
    if limit_int < 1 or limit_int > 500:
        return False
    return True