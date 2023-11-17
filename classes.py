import sqlite3 as sql
import datetime
conn =sql.connect("DataBase.dp")
c=conn.cursor()
class User:
    ID=0
    Username=''
    Email=''
    Password=''
    FullName=''
    PhoneNumber=''
    Age=0
    def Get(This,Data):
        This.ID=int(Data[0])
        This.Username=str(Data[1])
        This.FullName=str(Data[2])
        This.PhoneNumber=str(Data[3])
        This.Email=str(Data[4])
        This.Password=str(Data[5])
        This.Age=int(Data[6])
    

    def Login(This,Type):
        while True:
            UserName=input("Enter your UserName/ PhoneNumber/ Email or -1 to cancle:\n")
            if UserName=='-1':
                This.ID=-1
                return
            Password=input("Enter your Password:\n")
            sqript=f"""select rowid,* from {Type} where (UserName= "{UserName}" or PhoneNumber = "{UserName}" or Email = "{UserName}") and Password = "{Password}";"""
            c.execute(sqript)
            Data = c.fetchone()
            if Data == None:
                print("unvaled UserName or Password.")
            else:
                This.Get(Data)
                break
    def UniqueInput(This,Type,Attribute):
        while True:
            Thing=input(f"Enter a unique {Attribute} or -1 to cancle: ")
            sqript=f"select {Attribute} from {Type} where {Attribute} = {Thing};"
            c.execute(sqript)
            if(Thing =='-1'or c.fetchone() == None) :
                return Thing
            else :
                print('Not valed please ',end ='')

    def Register(This,Type):
        FullName=input("Enter your Name or -1 to cancle: ")
        if FullName=='-1':
            This.ID = -1
            return
        UserName=This.UniqueInput(Type,"UserName")
        if UserName =='-1':
            This.ID = -1
            return
        Email=This.UniqueInput(Type,"Email")
        if Email=='-1':
            This.ID = -1
            return
        PhoneNumber=This.UniqueInput(Type,"PhoneNumber")
        if PhoneNumber=='-1':
            This.ID = -1
            return
        Password=input("Enter your Password or -1 to cancle: ")
        if Password=='-1':
            This.ID = -1
            return
        sqript=f"""insert into {Type} (FullName,UserName,PhoneNumber,Email,Password) values ("{FullName}","{UserName}","{PhoneNumber}","{Email}","{Password}")"""
        c.execute(sqript)
        conn.commit()
        
        
class Professor(User):
    # what  
 
class Student(User):


class TeachingAssistants(User):

