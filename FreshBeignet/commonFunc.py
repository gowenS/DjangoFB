import random, string

def generateGameName():
    out=''
    for i in range(4):
        out+=(random.choice(string.ascii_uppercase))
    return out

# if __name__ == "__main__":
    # do something