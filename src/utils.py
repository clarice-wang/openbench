# parse the llm's returned string
def parser_find_list(astr):
    # slice the substring for the python list
    start = astr.find('[')
    end = astr.rfind(']')
    if start == -1 or end == -1:
        return ""
    return astr[start:end+1]

# default backbone config
DEFAULT_BACKBONE_CONFIG = {
    "model": "gpt-4o",
    "api_key": None,
    "end_point": None,
    "temp": 1.0,
    "top_p": 0.9,
}
