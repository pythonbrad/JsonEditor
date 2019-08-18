import json

def del_space(data_json):
    text = ''
    ####gu guillemet --> "
    gu = False
    for i in data_json:
        if gu == '"':
            text += i
            if gu:
                gu = False
            else:
                gu = True
        elif i in ['\n', '\t', '\r'] and not gu:
            pass
        else:
            text += i
    return text

def indent(data_json):
    #data_json = data_json.replace('\n','').replace('\t','').replace('\r')
    text = ''
    inc = 0
    ####gu guillemet --> "
    gu = False
    for i in data_json:
        if i == '"':
            text += i
            if gu:
                gu = False
            else:
                gu = True
        elif i == ',' and not gu:
            text += i
            text += '\n' + '\t' * inc
        elif i in ['{','['] and not gu:
            inc += 1
            text += i
            text += '\n' + '\t' * inc
        elif i in [']','}'] and not gu:
            inc -= 1
            text += '\n' + '\t' * inc
            text += i
        else:
            text += i
    return text

def correct_error_double_quote(data_json):
    new_json = ''
    ####sgu single_guillemet --> '
    ####dgu double_guillemet --> "
    sgu = False
    dgu = False
    for i in data_json:
        if i == '"' and not sgu:
            new_json += '"'
            if dgu:
                dgu = False
            else:
                dgu = True
        elif i == "'" and not dgu:
            new_json += '"'
            if sgu:
                sgu = False
            else:
                sgu = True
        elif sgu:
            if i == '"':
               new_json += "'"
            else:
                new_json += i
        else:
            new_json += i
    return new_json

def verify(data_json):
    try:
        json.loads(data_json)
        return True
    except Exception as error:
        return error
