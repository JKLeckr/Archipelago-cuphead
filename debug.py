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

def print_list(list: list) -> None:
    for item in list:
        print(item)
