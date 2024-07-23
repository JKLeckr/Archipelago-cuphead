def test_duplicates(list: list) -> int:
    seen = set()
    dups = []
    for x in list:
        if x in seen:
            dups.append(x)
        else:
            seen.add(x)
    print("Duplicates: "+str(dups))
    print("Total Duplicates: "+str(len(dups)))
    return len(dups)

def print_list_each_line(list: list) -> None:
    for item in list:
        print(item)

def print_list(list: list) -> None:
    res = "["
    first = True
    if list:
        for item in list:
            if not first:
                res += ","
            else:
                first = False
            res += str(item)
    res += "]"
    print(res)
