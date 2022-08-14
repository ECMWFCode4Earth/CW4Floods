# Miscvellaneous script for crowdwater project

def str_to_num(x):
    for i in range(7):
        if x == f"minus {i}":
            return -i
        elif x == f"plus {i}":
            return i
        else :
            pass