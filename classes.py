import sqlite3 as sql
import datetime
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
    def Fill(This,Data):
        This.ID=int(Data[0])
        This.Username=str(Data[1])
        This.FullName=str(Data[2])
        This.PhoneNumber=str(Data[3])
        This.Email=str(Data[4])
        This.Password=str(Data[5])
        This.Age=int(Data[6])
    
    def GetFromID(This,Type,RowID):
        sqript=f"""select from {Type} rowid,* where rowid = {RowID}"""
        c.execute(sqript)
        Data=c.fetchone()
        if Data == None:
            This.ID=-1
        else:
            This.Fill(Data)
            
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
                This.Fill(Data)
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
    Courses=[]
    def Fill(This):
        sqript=f"""select rowid,* from Courses where CourseProf = {This.ID}"""
        c.execute(sqript)
        data=c.fetchall()
        for i in range(len(data)):
            opj=Course()
            opj.Fill(data[i])
            This.Courses.append(opj)

    def CoursesViwe(This):
        for i in range(len(This.Courses)):
            # This.Courses[i].ProfSee()
        # select a course or -1 to cancel
        course=Checker(0,1000000000)
        if course ==-1:
            This.UI()
        else:
            l=-1
            r=len(This.Courses)+1
            while(l+1<r):
                
    def UI(This):
        
        # what you want to do 
        # 1- see courses and maneg them
        # 2- create a course
        # 3- maneg teaching assisters in your courses
        # 4-  
        To=-1
        while To==-1:
            To =Checker(1,3)
            if To ==-1:
                print('Not valed')
        if To ==1:
            
        # elif To==2:

        # elif To==3:

        # elif To==4:

class Answer:
    ID=0
    Text=''
    Student=0 
    Assignment=0
    Date=0
    Grade=-1
    def Fill(This,Data):
        This.ID=Data[0]
        This.Text=Data[1]
        This.Student=Data[3] 
        This.Assignment=Data[4]
        This.Date=datetime.datetime.strptime(Data[5],"%d-%m-%Y")
        This.Grade=Data[6]

class Assignment:
    ID=0
    Text=''
    StartDate=0
    EndDate=0
    FromProf=0
    FromTeach=0
    FromCourse=0
    Answers=[]
    def Fill(This,Data):
        This.ID=int(Data[0])
        This.Text=str(Data[1])
        This.FromCourse=int(Data[2])
        This.FromProf=int(Data[3])
        This.FromTeach=int(Data[4])
        This.StartDate=datetime.datetime.strptime(Data[5],"%d-%m-%Y")
        This.EndDate=datetime.datetime.strptime(Data[6],"%d-%m-%Y")
        # datetime_obj = datetime.datetime.strptime(date_string, date_format)
        sqript=f"""select rowid,* from Answers where Assignment ={This.ID}"""
        c.execute(sqript)
        data=c.fetchall()
        for i in range(len(data)):
            opj=Answer()
            opj.Fill(data[i])
            This.Answers.append(opj)

class Course:
    ID=0
    Name=''
    Description=''
    CourseProf=0
    Assignment=[]
    def Fill(This,Data):
        This.ID=Data[0]
        This.Name=Data[1]
        This.Description=Data[2]
        This.CourseProf=Data[3]
        sqript=f"""select rowid,* from Assignments where Course = {This.ID}"""
        c.execute(sqript)
        data=c.fetchall()
        for i in range(len(data)):
            obj=Assignment()
            obj.Fill(data[i])
            This.Assignment.append(obj)

class Student(User):


class TeachingAssistants(User):

