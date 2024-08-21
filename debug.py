from .auxiliary import format_list

def test_duplicates(ls: list) -> int:
    seen = set()
    dups = []
    for x in ls:
        if x in seen:
            dups.append(x)
        else:
            seen.add(x)
    print("Duplicates: "+str(dups))
    print("Total Duplicates: "+str(len(dups)))
    return len(dups)

def print_list_each_line(ls: list) -> None:
    for item in ls:
        print(item)

def print_list(ls: list) -> None:
    print(format_list(ls))
