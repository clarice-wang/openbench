def parser_find_list(astr):
    # slice the substring for the python list
    start = astr.find('[')
    end = astr.rfind(']')
    if start == -1 or end == -1:
        return ""
    return astr[start:end+1]
