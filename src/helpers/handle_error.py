import sys
sys.path.append("/Users/angel/Documents/MidBootcamp/mbc_core/src/helpers/")

from json_res import json_response

def handle_error(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args,**kwargs)
        except Exception as e:
            print("An error occurred")
            print(e)
            return json_response({"An error occurred: ":str(e)},500)
    wrapper.__name__ = fn.__name__
    return wrapper