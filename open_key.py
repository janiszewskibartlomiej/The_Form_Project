def read_key():
    with open('secret_k.txt', 'r') as f:
        key = f.readline()
    return key
