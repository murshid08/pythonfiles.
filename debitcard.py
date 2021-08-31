def testcard(c_number):
    c_number=list(c_number)
    debit=''

    for number in c_number:
        debit+=number

    def repeat(n):
        for i in range(0,len(n)-3):
            if n[i]==n[i+1]==n[i+2]==n[i+3]:
                return True
    if debit.startswith(('4','5','6')):
        if len(debit)==16:
            if debit.isdigit():
                if repeat(debit)==True:
                    return "card is invalid!, card number repeated continuesly try again!"
                else:
                    return "card is valid,move on"
            else:
                return "card is invalid! ,check the number is numeric or not"
        else:
            return "invalid card! ,number must be 16 number"
    else:
        return "invalid card ! card must be starts with 4 to 6"
print(testcard(input("enter card number:")))

