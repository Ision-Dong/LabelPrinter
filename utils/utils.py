import inspect


def convert_to_hex(command:str):
    data = []
    lines = [l for l in command.strip().split("\n")]
    for line in lines:
        data += [int("0x" + data, 16) for data in line.strip().split(" ")]
    return data

def is_chinese(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    else:
        return False

def encode_to_gbk(content:str):
    result = []
    for char in content.split("\n"):
        char = char.strip()
        lines = []
        for c in char:
            s = str(hex(ord(c))).replace("0x", "").upper()
            lines.append(s)
        result.append(" ".join(lines))

    return result

def handle_y_coordinate(f):

    location = []

    def wrapper(*args, **kwargs):
        bound_args = inspect.signature(f).bind(*args, **kwargs)
        bound_args.apply_defaults()
        target_args = dict(bound_args.arguments)
        location.append(target_args['x'])
        location.append(target_args['y'])
        print(location)
        return f(*args, **kwargs)


    return wrapper

if __name__ == '__main__':
    st = """S/N: 1234567890abcd1234567890 
    MN: 1234567890abcd1234567890
    MODEL CODE: DDDDDDDDDDDD3333333
    INPUT: DC5V/1A
    WWW.MOCOCHI.COM
    MADE IN CHINA   06/23"""
    for i in encode_to_gbk(st):
        print(i)



