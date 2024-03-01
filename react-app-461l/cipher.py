def checkInputs(inputText:str, N:int, D:int) -> None:
    # contstraints for N and D
    assert N > 0
    assert D == -1 or D == 1

    # The input text should contain characters between " and ~, inclusive
    for c in inputText:
        assert ord('"') <= ord(c) <= ord("~")

def encrypt(inputText:str, N:int, D:int) -> str:
    checkInputs(inputText, N, D)

    # checks complete, now start the encryption
    inputText = inputText[::-1]
    N = N % (ord("~") - ord('"') + 1)

    encrypted = []
    for c in inputText:
        newValAscii = (ord(c) + (N * D))
        if newValAscii > ord("~"):
            newValAscii = ord('"') + (newValAscii - ord("~") - 1)
        elif newValAscii < ord('"'):
            newValAscii = ord("~") - (ord('"') - (newValAscii + 1))
        encrypted.append(chr(newValAscii))

    return ''.join(encrypted)

def decrypt(inputText:str, N:int, D:int) -> str:
    checkInputs(inputText, N, D)

    # checks complete, now start the decryption
    inputText = inputText[::-1]
    N = N % (ord("~") - ord('"') + 1)

    decrypted = []
    for c in inputText:
        newValAscii = (ord(c) - (N * D))
        if newValAscii > ord("~"):
            newValAscii = ord('"') + (newValAscii - ord("~") - 1)
        elif newValAscii < ord('"'):
            newValAscii = ord("~") - (ord('"') - (newValAscii + 1))
        decrypted.append(chr(newValAscii))

    return ''.join(decrypted)