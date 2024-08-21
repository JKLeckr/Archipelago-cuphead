def count_in_list(e, ls: list):
    count = 0
    for el in ls:
        if el == e:
            count += 1
    return count

def format_list(ls: list) -> str:
    res = "["
    first = True
    if ls:
        for item in ls:
            if not first:
                res += ","
            else:
                first = False
            res += str(item)
    res += "]"
    return res

def scrub_list(a: list, b: set) -> list:
    newlist: list = []
    for item in a:
        if item in b:
            newlist.append(item)
    return newlist
