import sqlite3 as sql
import datetime
import main
def Checker(num1,num2,cancle):
    c1=" or -1 to cancele"
    b1=False
    if cancle==1:
        b1=True
    else:
        c1=''
    while True:
        num=input(f'Enter a number [{num1},{num2}]{c1}:\n')
        try:
            num=int(num)
            if (num>=num1 and num<=num2) or (num==-1 and b1) :
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
                This.FullFill(Data)
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
    def FullFill(This):
        This.Courses=[]
        sqript=f"""select rowid,* from Courses where CourseProf = {This.ID}"""
        c.execute(sqript)
        data=c.fetchall()
        for i in range(len(data)):
            opj=Course()
            opj.Fill(data[i])
            This.Courses.append(opj)

    def SelectedCourse(This,Course):
        # 1- students
        # 2- techers
        # 3- assignments 
        see=Checker(1,3,1)
        if see==-1:
            This.SeeCourses()
        
        elif see==1:
            if (len(This.Courses[Course].Students))==0:
                # no student in that course
                # press enter to cancle 
                input()
                This.SelectedCourse(Course)
            else:
                for i in range(len(This.Courses[Course].Students)):
                    print(f"{i+1}- Student ID: {This.Courses[Course].Students[i][0]}\nUser Name: {This.Courses[Course].Students[i][1]}")
                # select a student 
                Student=Checker(1,len(This.Courses[Course].Students),1)
                if Student==-1:
                    This.SelectedCourse(Course)
                else:
                    # do you want to kick this student 
                    # 1- yes 
                    # 2- no
                    kick=Checker(1,2,3)
                    if kick==1:
                        This.Courses[Course].KickStudent(Student-1)
                        This.FullFill()
                    else:
                        This.SelectedCourse(Course)

        elif see==2:
            if (len(This.Courses[Course].TeachingAssistants))==0:
                # no TeachingAssistants in that course
                # press enter to cancle 
                input()
                This.SelectedCourse(Course)
            else:
                for i in range(len(This.Courses[Course].TeachingAssistants)):
                    print(f"{i+1}- TeachingAssistants ID: {This.Courses[Course].TeachingAssistants[i][0]}\nUser Name: {This.Courses[Course].TeachingAssistants[i][1]}")
                # select a TeachingAssistants 
                TeachingAssistants=Checker(1,len(This.Courses[Course].TeachingAssistants),1)
                if TeachingAssistants==-1:
                    This.SelectedCourse(Course)
                else:
                    # do you want to kick this TeachingAssistants 
                    # 1- yes 
                    # 2- no
                    kick=Checker(1,2,3)
                    if kick==1:
                        This.Courses[Course].KickTeacher(TeachingAssistants-1)
                        This.FullFill()
                    else:
                        This.SelectedCourse(Course)

        elif see==3:
            # 1- see Assignments
            # 2- create assignments 
            To =Checker(1,2,1)
            if To ==-1:
                This.SelectedCourse(Course)
            elif To == 1:
                if len(This.Courses[Course].Assignments)==0:
                    # There are no Assignments here do you want to create
                    # 1- yes
                    # 2- no 
                    Create=Checker(1,2,3)
                    if Create==1:
                        This.Courses[Course].CreateAssignment()
                    else:
                        This.SelectedCourse(Course)
                else:
                    This.Courses[Course].ViweAssignments()
                    # select an Assignment
                    Assignment=Checker(1,len(This.Courses[Course].Assignments),1)
                    if Assignment==-1:
                        This.SelectedCourse(Course)
                    else:
                        This.SelectedAssignment(Course,Assignment)
            elif To ==2:
                This.Courses[Course].CreateAssignment()
                
    def SelectedAssignment(This,Course,Assignment):
        # 1- Change EndDate
        # 2- Show Answers
        # 3- Delete 
        Do=Checker(1,3,1)
        if Do==-1:
            This.SelectedCourse(Course)
        elif Do ==1:
            This.Courses[Course].Assignments[Assignment].ChangeEndDate()
        elif Do ==2:

        elif Do ==3:
            This.Courses[Course].Assignments[Assignment].Delete()
        

    def SeeCourses(This):
        if(len(This.Courses))==0:
            # You don't have any courses
            # 1- create one
            # 2- back 
            To=Checker(1,2,3)
            if To == 1:
                This.CreateCourse()
            elif To ==2:
                This.UI()
        else:
            for i in range(len(This.Courses)):
                print("----------------------------------------------------------------")
                print(f"{i+1}-")
                This.Courses[i].Viwe()
                print("----------------------------------------------------------------")
                # select course:
                Course=Checker(1,len(This.Courses),1)
                if Course==-1:
                    This.UI()
                else:
                    This.SelectedCourse(Course-1)

    def UI(This):
        
        # what you want to do 
        # 1- see courses and maneg them
        # 2- invites 
        # 3- create a course
        # 4- loge out
        To =Checker(1,4,2)
        if To ==1:
            This.CreateCourse()
        elif To==2:
            This.SeeCourses()
        elif To ==3:
            This.ShowInvitation()
        elif To==4:
            main.Start()
            
class Answer:
    ID=0
    Text=''
    Student=0 
    Assignment=0
    Registration=0
    Date=0
    Grade=-1
    
    def Fill(This,Data):
        This.ID=Data[0]
        This.Text=Data[1]
        This.Student=Data[3] 
        This.Assignment=Data[4]
        This.Registration=Data[5]
        This.Date=datetime.datetime.strptime(Data[6],"%d-%m-%Y")
        This.Grade=Data[7]

class Assignment:
    ID=0
    Text=''
    StartDate=0
    EndDate=0
    FromID=''
    FromName=''
    Type=''
    FromCourse=0
    Answers=[]

    def Viwe(This):
        print(f"Start Date: {This.StartDate}\nEnd Date: {This.EndDate}\nFrom {This.Type} {This.FromName}")
    
    def Fill(This,Data):
        This.Answers=[]
        This.ID=Data[0]
        This.Text=Data[1]
        This.FromCourse=Data[2]
        if Data[3]!=None:
            This.FromID=Data[3]
            This.Type='Professor'
        else:
            This.FromID=Data[4]
            This.Type='TeachingAssistants'
        sqript=f"""select Name from {This.Type} where rowid = {This.FromID}"""
        c.execute(sqript)
        This.FromName=c.fetchone()
        This.FromTeach=Data[4]
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
    Assignments=[]
    Students=[]
    TeachingAssistants=[]

    def Fill(This,Data):
        This.Assignments=[]
        This.Students=[]
        This.TeachingAssistants=[]
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
            This.Assignments.append(obj)
        sqript=f"""select Student from Registrations where Course ={This.ID}"""
        c.execute(sqript)
        for i in c.fetchall():
            sqript=f"""select UseName from Students where rowid = {i[0]}"""
            c.execute(sqript)
            c.fetchone()
            This.Students.append(i[0],c.fetchone())
        
        sqript=f"""select Teacher from Assistants where Course ={This.ID}"""
        c.execute(sqript)
        for i in c.fetchall():
            sqript=f"""select UseName from TeachingAssistants where rowid = {i[0]}"""
            c.execute(sqript)
            c.fetchone()
            This.Students.append(i[0],c.fetchone())

    def ViweAssignments(This):
        for i in range(len(This.Assignments)):
            print ("----------------------------------------------------------------")
            print(f"{i+1}-")
            This.Assignments[i].Viwe()
            print("----------------------------------------------------------------")
    
    def Viwe(This):
        print(f"Name: {This.Name}\n{This.Description}")

    def KickStudent(This,ID):
        sqript=f"""delete from Registrations Where Student = {ID}"""
        c.execute(sqript)
        conn.commit()
    
    def KickTeacher(This,ID):
        sqript=f"""delete from Assistants Where Teacher = {ID}"""
        c.execute(sqript)
        conn.commit()
            
    def Delete(This):
        sqript=f"""delete from Courses where rowid = {This.ID}"""
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Registrations where Course = {This.ID}"""
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Assistants where Course = {This.ID}"""
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Assignments where Course = {This.ID}"""
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Assignments where Course = {This.ID}"""
        c.execute(sqript)
        conn.commit()

class Student(User):

class TeachingAssistants(User):