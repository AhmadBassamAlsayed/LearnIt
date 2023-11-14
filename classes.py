import sqlite3 as sql
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
            PassWord=input("Enter your PassWord:\n")
            sqript=f"""select rowid,* from {Type} where (UserName= "{UserName}" or PhoneNumber = "{UserName}" or Email = "{UserName}") and PassWord = "{PassWord}";"""
            c.execute(sqript)
            data = c.fetchone()
            if data == None:
                print("unvaled UserName or PassWord.")
            else:
                This.Get(data)
                break
    def UniqueInput(This,Type,Attribute):
        while True:
            Thing=input(f"Enter a unique {Attribute}:")
            sqript=f"select {Attribute} from {Type} where {Attribute} = {Thing};"
            c.execute(sqript)
            if(c.fetchone()==None) :
                return Thing
            else :
                print('Not valed please ',end ='')

    def Register(This,Type):
        UserName=input("Enter a unique UserName:")
        while True:
            if This.Exists(Type,"UserName",UserName) == 1:
                print ("Enter a valed UserName:")
            else:
                break
        Email=input("Enter a unique Email:")
        while True:
            if This.Exists(Type,"Email",Email) == 1:
                print ("Enter a valed Email:")
            else:
                break
        
            
        

class Professor(User):


class Student(User):


class TeachingAssistants(User):

