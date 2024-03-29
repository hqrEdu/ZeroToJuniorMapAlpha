import re
from utility_functions.api_exceptions import BadRequest


def is_data_complete_for_post(data):
    return 'discord' in data and 'zip_code' in data and 'stack' in data


def is_discord_a_string(discord):
    return isinstance(discord, str)


def is_discord_correct_format(discord):
    '''Check if 'discord' id matches the correct pattern, ie. "Jan_123#3745"'''
    return re.findall("^.{3,32}#[0-9]{4}$", discord)


def is_stack_correct(stack):
    return stack.lower() in ["be", "fe"]


def prepare_data(data):
    data['stack'] = data['stack'].lower()
    return data


def verify_POST_request(request):
    data = request.json
    if not is_data_complete_for_post(data):
        raise BadRequest(detail="Data incomplete.")
    elif not is_discord_a_string(data['discord']):
        raise BadRequest(detail="'discord' id is incorrect type.")
    elif not is_discord_correct_format(data['discord']):
        raise BadRequest(detail="Incorrect discord ID format.")
    elif not is_stack_correct(data['stack']):
        raise BadRequest(detail="Unrecognisable stack type. Expected value: 'be' or 'fe'.")