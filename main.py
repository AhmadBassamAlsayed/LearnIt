import DataSet
import classes as cls
DataSet.SetDataBase()
def Checker(num1,num2):
    while True:
        num=input(f'Enter a number [{num1},{num2}] or -1 to cancele:\n')
        try:
            num=int(num)
            if (num>=num1 and num<=num2) or num==-1:
                return num 
            else :
                print('Not valed')
        except:
            print('Not valed')


def Start():
    # select who are you 
    # 1 taecher
    # 2 prof 
    # 3 student
    User=''
    Type=''
    to=Checker(1,3)
    if(to == -1):
        quit()
    if (to == 2):
        User = cls.Professor()
        Type='Professors'
    elif(User == 1 ):
        User = cls.TeachingAssistants()
        Type='TeachingAssistants'
    else :
        User=cls.Student()
        Type='Students'
    # 1- login
    # 2- register
    Where= Checker(1,2)
    if   Where == 1:
        User.Login(Type)
    elif Where == 2:
        User.Register(Type)
    else:
        quit()
    if User.ID==-1:
        Start()
    