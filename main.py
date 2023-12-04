import DataSet
import classes
import sqlite3 as sql
DataSet.SetDataBase()
conn =sql.connect("DataBase.dp")
c=conn.cursor()

def Checker(num1,num2,cancle):
    c1=" or -1 to cancele"
    b1=False
    if cancle==1:
        b1=True
    else:
        c1=''
    while True:
        num=input(f'Enter a number [{str(num1)},{str(num2)}]{str(c1)}:\n')
        try:
            num=int(num)
            if (num>=num1 and num<=num2) or (num==-1 and b1) :
                return num 
            else :
                print('Not valed')
        except:
            print('Not valed')

def Login():
    while True:
        UserName=input("Enter your UserName / Email or -1 to cancle:\n")
        if UserName=='-1':
            return -1
        Password=input("Enter your Password:\n")
        sqript=f"""select rowid,* from Users where (UserName= "{str(UserName)}" or Email = "{str(UserName)}") and Password = "{str(Password)}";"""
        c.execute(sqript)
        Data = c.fetchone()
        if Data == None:
            print("unvaled UserName or Password.")
        else:
            User=classes.User()
            if Data[5]=='P':
                User=classes.Professor()
            elif Data[5]=='S':
                User=classes.TeachingAssistants()
            elif Data[5]=='T':
                User=classes.Student()
            User.Fill(Data)
            return User

def UniqueInput(Attribute):
    while True:
        Thing=input(f"Enter a unique {str(Attribute)}: ")
        sqript=f"""select {str(Attribute)} from Users where {str(Attribute)} = "{str(Thing)}" ;"""
        c.execute(sqript)
        if(c.fetchone() == None) :
            return Thing
        else :
            print('Not valed please ',end ='')

def Register():
    print(" What is your psition")
    print(" 1- prof")
    print(" 2- stud")
    print(" 3- teacher")  
    Position=Checker(1,3,5)
    if Position==1:
        Position='P'
    if Position==2:
        Position='S'
    if Position==3:
        Position='T'
    FullName=input("Enter your Name:")
    UserName=UniqueInput("UserName")
    Email=UniqueInput("Email")
    Password=input("Enter your Password or -1 to cancle: ")
    sqript=f"""insert into Users (FullName,UserName,Email,Password,Position) values ("{str(FullName)}","{str(UserName)}","{str(Email)}","{str(Password)}","{str(Position)}")"""
    c.execute(sqript)
    conn.commit()

User=0
while True:
    print(" what do you want to ?")
    print(" 1- login")
    print(" 2- register")
    Choise=Checker(1,2,1)
    if Choise==-1 :
        quit()
    elif Choise==1:
        User=Login()
        if User==-1:
            continue
        User.UI()
    else:
        Register()
        print(" do you want to login ?")
        print(" 1- yes")
        print(" 2- no")
        Choise=Checker(1,2,1)
        if Choise==1:
            User=Login()
            User.UI()
            if User==-1:
                continue
        else:
            continue 
