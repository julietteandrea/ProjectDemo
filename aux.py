##### HELPFUL FUNCTION #####

"""sanitize/validate user phone number inputs."""
def sanitize(input_str):
    sanitized = input_str
    invalid_strs = ['(',')','-','input://','file://',';','<','>','$',
                    '../','table','TABLE','*','#',' ','_','/','@']

    for c in invalid_strs:
        if c in sanitized:
            sanitized = sanitized.replace(c,'')

    return sanitized

