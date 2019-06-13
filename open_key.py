def read_key():
    with open('session_k.txt', 'r') as f:
        key = f.readline()
    return key
