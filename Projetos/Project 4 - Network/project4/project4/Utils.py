import re
from django.contrib import messages
from django.contrib.messages import constants as message_constants
from django.contrib.messages.api import error

# for validating an Email
is_email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

#Strings Validations
def strIsBlank (str):
    return not (str and str.strip())

def strIsWhitespace (str):
    return str.isspace()

def strIsNone(str):
    return str == None 

def strIsNoneBlankWhithespace(str):
    return (strIsNone(str) or strIsWhitespace(str) or strIsBlank(str))


def contains_errormessage(request):
    storage = messages.get_messages(request)
    for msg in storage:
        if (msg.level == message_constants.ERROR):
            return True
    return False

def is_email(str):
    if(re.search(is_email_regex, str)):
        return True
    else:
        return False

def is_image(image):
    
    if (image is None):
        return False
    if (image.size <= 0):
        return False
    # other checkings?
    return True
