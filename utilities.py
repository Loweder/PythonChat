from animcode import animator as an


def unphase(text: str) -> list:
    data = []
    old_made = ""
    remade = text
    while True:
        info = ""
        if old_made == remade:
            return data
        old_made = remade
        for let in remade:
            if let == ":":
                remade = remade[remade.index(":") + 1:]
                break
            info = info + let
        data.append(type_to(info))
def rephase(data: list) -> list:
    result = []
    for d in data:
        result.append(type_to(type_of(d) + str(d)))
    return result
def phase(data: list) -> str:
    text = ""
    for d in data:
        text = text + type_of(d)
        text = text + str(d)
        if data.index(d) != len(data) - 1:
            text = text + ":"
    return text

def type_of(o: object) -> str:
    if type(o) == int:return "i&"
    elif type(o) == float:return "f&"
    elif type(o) == complex:return "c&"
    elif type(o)== dict:return "d&"
    elif type(o) == set:return "S&"
    elif type(o) == bool:return "B&"
    elif type(o) == tuple:return "t&"
    elif type(o) == list:return "l&"
    elif type(o) == str:
        try:
            int(str(o))
            return "i&"
        except ValueError:
            print(o)
        try:
            float(str(o))
            return "f&"
        except ValueError:
            pass
        try:
            complex(str(o))
            return "c&"
        except ValueError:
            pass
        if str(o) == "True" or str(o) == "False":
            return "B&"
        return "s&"


def type_to(val: str):
    typecode = ""
    for let in val:
        if let == "&":break;
        typecode = typecode + let
    if typecode == "i":return int("".join(val[2:]))
    elif typecode == "f":return float("".join(val[2:]))
    elif typecode == "c":return complex("".join(val[2:]))
    elif typecode == "d":return dict(eval(val[2:]))
    elif typecode == "S":return set(eval(val[2:]))
    elif typecode == "B":return True if "".join(val[2:]) == "True" else False
    elif typecode == "t":return tuple(eval(val[2:]))
    elif typecode == "l":return list(eval(val[2:]))
    elif typecode == "s":return str("".join(val[2:]))
    else:return val
def is_uid(value: int):
    if type(value) == int:return True
    return False

def alterMessage(message: str):
    an.add(28, message)
    an.rem(2)