import cipher

def testHW2():

    userIDs=['"asamant~']
    passwords=["Temp123"]
    for i in range(1):
        text1=userIDs[i]
        text2=passwords[i]

        s=3
        d=-1
        encrypteduserid=cipher.encrypt(text1, s, d)
        encryptedpasswd=cipher.encrypt(text2, s, d)
        print("Encrypted User ID: ", encrypteduserid)

        originaluserid=cipher.decrypt(encrypteduserid, s, d)
        originalpasswd=cipher.decrypt(encryptedpasswd, s, d)
        if((text1==originaluserid)&(text2==originalpasswd)):
            print("Test Passed")
        else:
            print("Test Failed")
        
    
def main():
    print("Running HW2 tests......")
    testHW2()
    
main()