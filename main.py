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
        num=input(f'Enter a number [{(num1)},{(num2)}]{(c1)}:\n')
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
        sqript=f"""select rowid,* from Users where (UserName= "{(UserName)}" or Email = "{(UserName)}") and Password = "{(Password)}";"""
        c.execute(sqript)
        Data = c.fetchone()
        if Data == None:
            print("unvaled UserName or Password.")
        else:
            User=classes.User()
            if Data[5]=='P':
                User=classes.Professor()
            elif Data[5]=='S':
                User=classes.Teacher()
            elif Data[5]=='T':
                User=classes.Student()
            User.Fill(Data)
            return User

def UniqueInput(Attribute):
    while True:
        Thing=input(f"Enter a unique {(Attribute)}: ")
        sqript=f"select {(Attribute)} from Users where {(Attribute)} = {(Thing)};"
        c.execute(sqript)
        if(c.fetchone() == None) :
            return Thing
        else :
            print('Not valed please ',end ='')

def Register():
    # What is your psition
    # 1- prof
    # 2- stud
    # 3- teacher  
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
    sqript=f"""insert into Users (FullName,UserName,Email,Password,Position) values ("{(FullName)}","{(UserName)}","{(Email)}","{(Password)}","{(Position)}")"""
    c.execute(sqript)
    conn.commit()


User=0
while True:
    # what do you want to ?
    # 1- login
    # 2- register
    Choise=Checker(1,2,1)
    if Choise==-1 :
        quit()
    elif Choise==1:
        User=Login()
        if User==-1:
            continue
    else:
        Register()
        # do you want to login ?
        # 1- yes
        # 2- no
        Choise=Checker(1,2,1)
        if Choise==1:
            User=Login()
            if User==-1:
                continue
        else:
            continue 
