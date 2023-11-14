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
    def Get(This,data):
        This.Age=
        This.Email=
        This.FullName=
        This.Password=
        This.ID=
    def Login(This,Type):
        while True:
            UserName=input("Enter your UserName/ PhoneNumber/ Email or -1 to cancle:\n")
            if UserName=='-1':
                This.Age=-1
                return
            PassWord=input("Enter your PassWord:\n")
            sqript=f"""select rowid,* from {Type} where (UserName= "{UserName}" or PhoneNumber = "{UserName}" or Email = "{UserName}" and PassWord = "{PassWord}";"""
            c.execute(sqript)
            data = c.fetchone()
            if data == None:
                print("unvaled UserName or PassWord")
            else:
                This.Get(data)

class Professor(User):


class Student(User):


class TeachingAssistants(User):

