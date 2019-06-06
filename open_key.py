def klucz():
    with open('session_k.txt', 'r') as f:
        key = f.readline()
    return key
