import sqlite3 as sql
from datetime import datetime,timedelta
conn =sql.connect("DataBase.dp")
c=conn.cursor()

def JoinTables(TableA,TableB,FromTableA,FromTableB,MatchFromA,MachFromB,OneOrAll):
    sqript=f"""SELECT {str(TableA)}.{str(FromTableA)}, {str(TableB)}.{str(FromTableB)} FROM {str(TableA)} INNER JOIN {str(TableB)} ON {str(TableA)}.{str(MatchFromA)} = {str(TableB)}.{str(MachFromB)}"""
    c.execute(sqript)
    Data=[]
    if OneOrAll==1:
        Data=c.fetchone()
    else:
        Data=c.fetchall()
    return Data

def FetchFromData(Table,Atributes,OneOrAll,Where):
    sqript=f"""select {str(Atributes)} from {str(Table)} where {str(Where)}"""
    c.execute(sqript)
    Data=0
    if OneOrAll==1:
        Data=c.fetchone()
    else:
        Data=c.fetchall()
    return Data

def InsertIntoData(Table,Atriputes,Values):
    sqript=f"""insert into {str(Table)} ({str(Atriputes)}) values ({str(Values)})"""
    c.execute(sqript)
    conn.commit()

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

class User:
    ID=0    
    Username=''
    Email=''
    Password=''
    FullName=''
    Position=''

    def Delete(This):
        sqript=f"""delete from Users where rowid = {This.ID}"""
        c.execute(sqript)
        conn.commit()
        
        sqript=f"""delete from Invitations where Professor = {This.ID} or Professor = {This.ID}"""
        c.execute(sqript)
        conn.commit()
        
        sqript=f"""delete from Answers where Student = {This.ID}"""
        c.execute(sqript)
        conn.commit()

        sqript=f"""delete from Messages where FromWho = {This.ID} or ToWho = {This.ID}"""
        c.execute(sqript)
        conn.commit()

        

    def InBoX(This):
        while True:
            Data=FetchFromData("Messages","rowid,*",2,f"ToWho = {str(This.ID)} ")
            Messages=[]
            for i in Data:
                opj = Message()
                opj.Fill(i)
                Messages.append(opj)
            if len(Data)==0:
                input("Empty")
                return
            else:
                for i in range(len(Messages)):
                    print("----------------------------------------------------------------")
                    print(f"{str(i+1)}-\n")
                    Messages[i].Viwe()
                    print("----------------------------------------------------------------")
                    
                print(" select a Message")
                ThisMessage=Checker(1,len(Messages),1)
                if ThisMessage==-1:
                    return
                else:
                    MessageIndex=ThisMessage-1
                    while True:
                        print(" 1- delete")
                        print(" 2- Message The Sender")
                        Choise=Checker(1,2,1)
                        if Choise==-1:
                            break
                        elif Choise==1:
                            Messages[MessageIndex].Delete()
                            break
                        elif Choise==2:
                            This.CreateMessage(Messages[MessageIndex].FromWho)

    def OutBox(This):
        while True:
            Data=FetchFromData("Messages","rowid,*",2,f"FromWho = {str(This.ID)} ")
            Messages=[]
            for i in Data:
                opj = Message()
                opj.Fill(i)
                Messages.append(opj)
            if len(Data)==0:
                input("Empty")
                return
            else:
                for i in range(len(Messages)):
                    print("----------------------------------------------------------------")
                    print(f"{str(i+1)}-\n")
                    Messages[i].Viwe()
                print(" select a Message")
                ThisMessage=Checker(1,len(Messages),1)
                if ThisMessage==-1:
                    return
                else:
                    MessageIndex=ThisMessage-1
                    while True:
                        print(" 1- delete")
                        print(" 2- Message The Reciver")
                        Choise=Checker(1,2,1)
                        if Choise==-1:
                            break
                        elif Choise==1:
                            Messages[MessageIndex].Delete()
                            break
                        elif Choise==2:
                            This.CreateMessage(Messages[MessageIndex].ToWho)

    def Fill(This,Data):
        This.ID=int(Data[0])
        This.Username=str(Data[1])
        This.FullName=str(Data[2])
        This.Email=str(Data[3])
        This.Password=str(Data[4])
        This.Position=str(Data[5])
    
    def CreateMessage(This,To):
        Text=input("Enter The Message")
        if FetchFromData("Users","UserName",1,f"rowid = {To}")==None:
            print("Deleted Account")
            return

        InsertIntoData("Messages"," FromWho, ToWho, Message",f"""{str(This.ID)},{str(To)},"{str(Text)}" """)
        
class Message:
    ID=0
    FromWho=0
    FromType=''
    FromName=''
    ToWho=0
    ToType=''
    ToName=''
    Text=''

    def Fill(This,Data):
        This.ID=Data[0]
        This.FromWho=Data[1]
        cur=FetchFromData("Users","UserName,Position",1,f"rowid = {str(This.FromWho)}")
        This.FromName=cur[0]
        if cur[1]=='T':
            This.FromType="Teacher"
        if cur[1]=='P':
            This.FromType="Professor"
        if cur[1]=='S':
            This.FromType="Student"
        This.ToWho=Data[2]
        cur=FetchFromData("Users","UserName,Position",1,f"rowid = {str(This.ToWho)}")
        This.ToName=cur[0]
        if cur[1]=='T':
            This.ToType="Teacher"
        if cur[1]=='P':
            This.ToType="Professor"
        if cur[1]=='S':
            This.ToType="Student"
        This.Text=Data[3]
    
    def Delete(This):
        sqript=f"""delete from Messages where rowid = {str(This.ID)}"""
        c.execute(sqript)
        conn.commit()

    def Viwe(This):
        print(f"From {str(This.FromType)}: {str(This.FromName)}\nTo {str(This.ToType)}: {str(This.ToName)}\n{str(This.Text)}\n")

class Professor(User):

    def CreateCourse(This):
        Name=input("Enter The Cousre Name:")
        Discription=input("Enter The Course Discription:")
        print(" 1- confirm the creation")
        print(" 2- cnacle  ")
        Choise=Checker(1,2,2)
        if Choise==1:
            InsertIntoData("Courses","Name, Description, CourseProf ",f""" "{str(Name)}", "{str(Discription)}",{str(This.ID)} """)
        else:
            return
    
    def CreateInvite(This,Course):
        AvTeachers=[]
        sqript=f"""select rowid,UserName from Users where Position = "T" and not exists 
        (select * from Invitations where TeachingAssistant = Users.rowid and Course = {Course.ID})
        and not exists
        (select * from Assistants where Teacher = Users.rowid and Course = {Course.ID});"""
        c.execute(sqript)
        AvTeachers=c.fetchall()
        for i in range(len(AvTeachers)):
            print("----------------------------------------------------------------")
            print(f"{str(i+1)}-\n\t{str(AvTeachers[i][1])}")
            print("----------------------------------------------------------------")
        if len(AvTeachers)==0:
            input("Empty")
            return
        print(" select a teacher")
        Teacher=Checker(1,len(AvTeachers),1)
        if Teacher==-1:
            return
        else:
            TeacherID=AvTeachers[Teacher-1][0]
            Message=input("type a message dont let it empty:")
            if Message=='':
                Message ='Empty Message!'
            InsertIntoData("Invitations","Message, Professor, Course, TeachingAssistant",f""" "{str(Message)}", {str(This.ID)},{str(Course.ID)},{str(TeacherID)} """)
            print(" Done")
            return
    
    def SelectedStudent(This,Course,StudentID):
        while True:
            print(" 1- kick")
            print(" 2- Message ")
            Choise=Checker(1,2,1)
            if Choise==-1:
                return
            elif Choise==1:
                Course.KickStudent(StudentID)
                return
            elif Choise==2:
                This.CreateMessage(StudentID)
            
    def ShowStudents(This,Course):
        while True:
            AvStudents=[]
            sqript =f"""select rowid,UserName from Users where exists (select * from Registrations where Student = Users.rowid and Course = {str(Course.ID)} );"""
            c.execute(sqript)
            AvStudents=c.fetchall()
            for i in range(len(AvStudents)):
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-\n\t{str(AvStudents[i][1])}")
                print("----------------------------------------------------------------")
            if len(AvStudents)==0:
                input("Empty")
                return
            print(" select a Student")
            Student=Checker(1,len(AvStudents),1)
            if Student==-1:
                return
            else:
                StudentID=AvStudents[Student-1][0]
                This.SelectedStudent(Course,StudentID)

    def SelectedTeacher(This,Course,TeacherID):
        print(" 1- message him ")
        print(" 2- kick him From This Course")
        Choise=Checker(1,2,1)
        if Choise==-1:
            return
        elif Choise==1:
            This.CreateMessage(TeacherID)
        elif Choise==2:
            Course.KickTeacher(TeacherID)

    def ShowTeachers(This,Course):
        while True:    
            sqript=f"""select rowid,UserName from Users where exists (select * from Assistants Where Teacher = Users.rowid and Course={str(Course.ID)})"""
            c.execute(sqript)
            Teachers=c.fetchall()
            if len(Teachers)==0:
                input("Empty")
                return
            for i in range(len(Teachers)):
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-\n\t{str(Teachers[i][1])}")
                print("----------------------------------------------------------------")
            print(" select a Teacher ")
            Teacher=Checker(1,len(Teachers),1)
            if Teacher==-1:
                return
            else:
                TeacherID=Teacher-1
                This.SelectedTeacher(Course,TeacherID)

    def SelectedAssignment(This,ThisAssignment):
        while True:
            print(" 1- UnGraded Answers")
            print(" 2- Greded Aswers")
            print(" 3- delete ")
            print(" 4- Add Extra Time")
            Choise=Checker(1,4,1)
            if Choise==-1:
                return
            elif Choise==1:
                ThisAssignment.NotGradedAnswers(This)
            elif Choise==2:
                ThisAssignment.GradedAnswers(This)
            elif Choise==3:
                print(" Are you sure ?")
                print(" 1- Yes")
                print(" 2- cancle ")
                Choise=Checker(1,2,3)
                if Choise==1:
                    ThisAssignment.Delete()
                    break
                else:
                    continue
            elif Choise==4:
                ThisAssignment.ExtraTime()

    def ShowAssignments(This,Course):
        while True:
            Data =FetchFromData("Assignments","rowid,*" ,2,f"Course = {str(Course.ID)} ")
            if len(Data)==0:
                input("Empty")
                return
            else:
                Assignments=[]
                for i in range(len(Data)):
                    opj=Assignment()
                    opj.Fill(Data[i])
                    Assignments.append(opj)
                for i in range(len(Assignments)):
                    print ("----------------------------------------------------------------")
                    print(f"{str(i+1)}-")
                    Assignments[i].Viwe()
                    print ("----------------------------------------------------------------")
                print(" select an Assignment")
                ThisAssignment=Checker(1,len(Assignments),1)
                if ThisAssignment==-1:
                    return
                else:
                    AssignmentID=ThisAssignment-1
                    This.SelectedAssignment(Assignments[AssignmentID])

    def SelectedCourse(This,Course):
        while True:
            print(" 1- send invite")
            print(" 2- Show Students")
            print(" 3- Show Teachers")
            print(" 4- Show Assignments")
            print(" 5- Add Assignment")
            print(" 6- Delete Course")
            Choise=Checker(1,6,1)
            if Choise==-1:
                return
            elif Choise==1:
                This.CreateInvite(Course)
            elif Choise==2:
                This.ShowStudents(Course)
            elif Choise==3:
                This.ShowTeachers(Course)
            elif Choise==4:
                This.ShowAssignments(Course)
            elif Choise==5:
                ThisAssignment=Assignment()
                ThisAssignment.CreateAssignment(This.ID,Course.ID)
            elif Choise==6:
                print(" Are You Sure?")
                print(" 1- yes ")
                print(" 2- no")
                Choise=Checker(1,2,3)
                if Choise==1:
                    Course.Delete()
                    break

    def SeeCourses(This):
        while True:
            Data=FetchFromData("Courses","rowid,*",2,f"CourseProf = {str(This.ID)}")
            Courses=[]
            for i in Data:
                opj=Course()
                opj.Fill(i)
                Courses.append(opj)
            if len(Courses)==0:
                input("Empty")
                return
            for i in range(len(Courses)):
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-")
                Courses[i].Viwe()
                print("----------------------------------------------------------------")
            print(" select a course")
            Choise=Checker(1,len(Courses),1)
            if Choise==-1:
                return
            else:
                This.SelectedCourse(Courses[i-1])

    def ShowInvitations(This):
        while True:
            Data=FetchFromData("Invitations" ,"rowid,*",2,f"Professor = {str(This.ID)}")
            if len(Data)==0:
                input("Empty")
                return
            else:
                Invitations=[]
                for i in range(len(Data)):
                    opj=Invitation()
                    opj.Fill(Data[i])
                    print("----------------------------------------------------------------")
                    print(f"{str(i+1)}-\n")
                    opj.Viwe()
                    Invitations.append(opj)
                    print("----------------------------------------------------------------")
                print(" select an Invitation")
                ThisInvitation=Checker(1,len(Invitations),1)
                if ThisInvitation==-1:
                    return
                else:
                    ThisInvitation=Invitations[ThisInvitation-1]
                    while True:
                        print(" 1- Message The Teacher")
                        print(" 2- cancle The invitation")
                        Choise=Checker(1,2,1)
                        if Choise==-1: 
                            break
                        elif Choise==1:
                            This.CreateMessage(ThisInvitation.ToWho)
                        elif Choise==2:
                            print(" are you sure")
                            print(" 1- yes")
                            print(" 2- no ")
                            Cancle=Checker(1,2,3)
                            if Cancle==1:
                                ThisInvitation.Cancle()
                                return
    
    def UI(This):
        while True:
            print(" what you want to do ")
            print(" 1- see courses and maneg them")
            print(" 2- invites ")
            print(" 3- create a course ")
            print(" 4- Inbox")
            print(" 5- OutBox ")
            print(" 6- loge out")
            print(" 7- Delete account")
            To =Checker(1,7,2)
            if To ==1:
                This.SeeCourses()
            elif To==2:
                This.ShowInvitations()
            elif To ==3:
                This.CreateCourse()
            elif To==4:
                This.InBoX()
            elif To == 5:
                This.OutBox()
            elif To == 6:
                return
            elif To==7:
                This.Delete()
                return
            
class Answer:
    ID=0
    Text=''
    Student=0 
    Assignment=0
    Registration=0
    SubmitDate=None
    Grade=-1
    StudentName="DeletedAccount"
    GradeMessage=''

    def Submit(This):
        Date=datetime.strptime(FetchFromData("Assignments","EndDate",1,f"rowid = {str(This.Assignment)}")[0],"%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        if now<=Date:
            sqript=f"""update Answers set SubmitDate = "{now.strftime("%Y-%m-%d %H:%M:%S")}"  """
            c.execute(sqript)
            conn.commit()
        else:
            input("sorry there is no Time ); ")

    def Fill(This,Data):
        This.ID=Data[0]
        This.Text=Data[1]
        This.Student=Data[2] 
        This.Assignment=Data[3]
        This.Registration=Data[4]
        This.SubmitDate=datetime.strptime(Data[5],"%Y-%m-%d %H:%M:%S")
        This.Grade=Data[6]
        This.GradeMessage=Data[7]
        if FetchFromData("Users"," UserName ",1,f"""rowid = {str(This.Student)}""")!=None:
            This.StudentName=FetchFromData("Users"," UserName ",1,f"""rowid = {str(This.Student)}""")[0]
    
    def Viwe(This):
        print(f"From: {str(This.StudentName)}\nDate: {str(This.SubmitDate)}\nAnswer:\n{str(This.Text)}")
        if This.Grade==-1:
            print("Not Graded")
        else:
            print(f"Grade: {str(This.Grade)}/10 \nMessage: {This.GradeMessage}")
    
    def MakeGrade(This):
        print(" Enter The grade")
        Grade=Checker(0,10,1)
        if Grade==-1:
            return
        else:
            This.Grade=Grade
            Message=input("Enter The MEssage")
            if Message=='':
                Message="NO MEssage!?"
            sqript=f"""update Answers set Grade = {str(This.Grade)}, GradeMessage = "{str(Message)}" WHERE rowid = {str(This.ID)};"""
            c.execute(sqript)
            conn.commit()
    
    def NotGraded(This,User):
        while True:
            print(" 1- Grade")
            print(" 2- Message Student")
            Choise=Checker(1,2,1)
            if Choise==-1:
                return
            elif Choise==1:
                This.MakeGrade()
                break
            elif Choise==2:
                User.CreateMessage(This.Student)
    
    def Graded(This,User):
        while True:
            print(" 1- ChangeGrade")
            print(" 2- Message Student")
            Choise=Checker(1,2,1)
            if Choise==-1:
                return
            elif Choise==1:
                This.MakeGrade()
            elif Choise==2:
                User.CreateMessage(This.Student)

class Assignment:
    ID=0
    Text=''
    StartDate=''
    EndDate=''
    FromID=0
    FromName="DeletedAccount"
    FromCourse=0
    
    def Fill(This,Data):
        This.ID=Data[0]
        This.Text=Data[1]
        This.FromCourse=Data[2]
        This.FromID=Data[3]
        This.StartDate=datetime.strptime(Data[4],"%Y-%m-%d %H:%M:%S")
        This.EndDate=datetime.strptime(Data[5],"%Y-%m-%d %H:%M:%S")
        if FetchFromData("Users"," UserName ",1,f"""rowid = {str(This.FromID)}""")!=None:
            This.FromName=FetchFromData("Users"," UserName ",1,f"""rowid = {str(This.FromID)}""")[0]

    def CreateAssignment(This,FromID,FromCourse):
        Text=input("Enter The Assignment and Press \'Enter\' to conferm it and DONT USE (\") :\n")
        StartDate=datetime.now()
        StartDate=datetime.strptime(StartDate.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
        EndDate=StartDate
        while StartDate>=EndDate:
            Date=input("Enter The end date in format (YYYY-MM-DD) and it has to be at les tommorow: ")
            try:
                EndDate=datetime.strptime(Date,'%Y-%m-%d')
            except:
                print("Error")
                continue
        sqript=f"""insert into Assignments (Assignment,Course,Creater,StartDate,EndDate) values ("{str(Text)}",{str(FromCourse)},{str(FromID)},"{str(StartDate)}","{str(EndDate)}")"""
        c.execute(sqript)
        conn.commit()
    
    def Viwe(This):
        print(f"Creater: {str(This.FromName)}\nStartDate: {str(This.StartDate)}\nEndDate: {str(This.EndDate)}\n{str(This.Text)}")

    def NotGradedAnswers(This,User):
        Data=FetchFromData("Answers"," rowid,* ",2,f"""Assignment = {str(This.ID)} and Grade = -1 and SubmitDate !="2000-01-01 00:00:00" """ )
        Answers=[]
        # print(This.ID)
        if len(Data)==0:
            input("Empty")
            return
        for i in range(len(Data)):
            opj=Answer()
            opj.Fill(Data[i])
            Answers.append(opj)
            print ("----------------------------------------------------------------")
            print(f"{str(i+1)}-")
            opj.Viwe()
            print ("----------------------------------------------------------------")
        print(" select an Answer")
        ThisAnswer=Checker(1,len(Answers),1)
        if ThisAnswer==-1:
            return
        else:
            AnswerID=ThisAnswer-1
            Answers[AnswerID].NotGraded(User)
     
    def GradedAnswers(This,User):
        Data=FetchFromData("Answers"," rowid,* ",2,f"""Assignment = {str(This.ID)} and SubmitDate != "2000-01-01 00:00:00" and Grade != -1  """ )
        Answers=[]
        if len(Data)==0:
            input("Empty")
            return
        for i in range(len(Data)):
            opj=Answer()
            opj.Fill(Data[i])
            Answers.append(opj)
            print ("----------------------------------------------------------------")
            print(f"{str(i+1)}-")
            opj.Viwe()
            print ("----------------------------------------------------------------")
        print(" select an Answer")
        ThisAnswer=Checker(1,len(Answers),1)
        if ThisAnswer==-1:
            return
        else:
            AnswerID=ThisAnswer-1
            Answers[AnswerID].Graded(User)
                
    def Delete(This):
        sqript=f"delete from Assignments where rowid = {str(This.ID)}"
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Answers Where Assignment ={str(This.ID)} """
        c.execute(sqript)
        conn.commit()

    def ExtraTime(This):
        now = datetime.now()
        if This.EndDate <now:
            input("sorry now Time );")
            return
        Time=0
        while Time<=0:
            Time=input("Enter a positiv Number or -1 to cancle")
            if Time=='-1':
                return
            try:
                Time=int(Time)

            except:
                Time=0
                continue
        NewEndDate=datetime.now()
        NewEndDate = This.EndDate + timedelta(Time)
        This.EndDate=NewEndDate
        sqript=f"""update Assignments set EndDate = "{str(NewEndDate)}" where rowid = {str(This.ID)}"""
        # print (sqript)
        c.execute(sqript)
        conn.commit()

class Course:
    ID=0
    Name=''
    Description=''
    CourseProf=0

    def Fill(This,Data):
        This.ID=Data[0]
        This.Name=Data[1]
        This.Description=Data[2]
        This.CourseProf=Data[3]

    def Viwe(This):
        print(f"Name: {str(This.Name)}\n{str(This.Description)}")

    def KickStudent(This,ID):
        sqript=f"""delete from Registrations Where Student = {str(ID)}"""
        c.execute(sqript)
        conn.commit()
    
    def KickTeacher(This,ID):
        sqript=f"""delete from Assistants Where Teacher = {str(ID)}"""
        c.execute(sqript)
        conn.commit()
            
    def Delete(This):
        sqript=f"""delete from Courses where rowid = {str(This.ID)}"""
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Registrations where Course = {str(This.ID)}"""
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Assistants where Course = {str(This.ID)}"""
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Assignments where Course = {str(This.ID)}"""
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Invitations where Course = {str(This.ID)}"""
        c.execute(sqript)
        conn.commit()

class Student(User):

    def MakeAnswer(This,ThisAssignmet):
        while True:
            Text=input("enter The Answer:\n")
            if len(Text)!=0:
                break
        print(" do you want to supmit it?")
        print(" 1- yes")
        print(" 2- no ")
        Choise=Checker(1,2,3)
        # print(f"Student = {str(This.ID)} and Course = {str(ThisAssignmet.FromCourse)}")
        # print(FetchFromData("Registrations","rowid",1,f"Student = {str(This.ID)} and Course = {str(ThisAssignmet.FromCourse)}"))
        regesteration=FetchFromData("Registrations","rowid",1,f"Student = {str(This.ID)} and Course = {str(ThisAssignmet.FromCourse)}")[0]
        InsertIntoData("Answers"," Answer, Student, Assignment, Registration ",f""" "{Text}",{str(This.ID)},{str(ThisAssignmet.ID)},{str(regesteration)} """)
        if Choise==1:
            Data=FetchFromData("Answers","rowid,*",1,f"Student = {str(This.ID)} and Assignment = {str(ThisAssignmet.ID)}")
            MyAnswer=Answer()
            MyAnswer.Fill(Data)
            MyAnswer.Submit()

    def SelectedAssignment(This,ThisAssignment):
        while True:
            Data = FetchFromData("Answers","rowid,*",1,f" Assignment = {ThisAssignment.ID} and Student = {This.ID} ")
            if Data == None:
                print(" do you want to answer?")
                print(" 1- yes")
                print(" 2- no")
                choise=Checker(1,2,3)
                if choise==1:
                    This.MakeAnswer(ThisAssignment)
                else:
                    return
            else:
                MyAnswer = Answer()
                MyAnswer.Fill(Data)
                # print(MyAnswer.SubmitDate)
                if MyAnswer.SubmitDate.strftime("%Y-%m-%d %H:%M:%S")=="2000-01-01 00:00:00":
                    print(" do you want to submit?")
                    print(" 1- yes")
                    print(" 2- no ")
                    choise=Checker(1,2,3)
                    if choise==1:
                        MyAnswer.Submit()
                    return
                else:
                    if MyAnswer.Grade== -1:
                        input(" not Graded yet")
                        return
                    else:
                        print(" Your Grage is:")
                        print(MyAnswer.Grade,end=f"/10\nMessage: {MyAnswer.GradeMessage}\n")

    def CourseTeachers(This,Course):
        while True:
            sqript=f""" select rowid,UserName from Users where exists (select * from Assistants Where Teacher = Users.rowid and Course={str(Course.ID)}); """
            c.execute(sqript)
            Teachers=c.fetchall()
            if len(Teachers)==0:
                input("Empty")
                return
            for i in range(len(Teachers)):
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-\nUserName: {str(Teachers[i][1])}\n")
                print("----------------------------------------------------------------")
            print(" select a Teacher")
            ThisTeacher=Checker(1,len(Teachers),1)
            if ThisTeacher==-1:
                return
            else:
                while True:
                    print(" 1- Message ")
                    print(" 2- cancle")
                    Choise=Checker(1,2,3)
                    if Choise==1:
                        This.CreateMessage(Teachers[ThisTeacher-1][0])
                    elif Choise==2:
                        break
        
    def CourseStudents(This,Course):
        while True:
            sqript=f""" select rowid,UserName from Users where exists (select * from Registrations Where Student = Users.rowid and Course = {str(Course.ID)} and Student != {str(This.ID)}); """
            c.execute(sqript)
            Students=c.fetchall()
            if len(Students)==0:
                input("Empty")
                return
            for i in range(len(Students)):
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-\nUserName: {str(Students[i][1])}\n")
                print("----------------------------------------------------------------")
            print(" select a Student")
            ThisStudent=Checker(1,len(Students),1)
            if ThisStudent==-1:
                return
            else:
                while True:
                    print(" 1- Message ")
                    print(" 2- cancle")
                    Choise=Checker(1,2,3)
                    if Choise==1:
                        This.CreateMessage(Students[ThisStudent-1][0])
                    elif Choise==2:
                        break

    def MyCourses(This):
        while True:
            sqript=f"""select rowid,* from Courses where exists(select * from Registrations where Course = Courses.rowid and Student = {This.ID});"""
            c.execute(sqript)
            Data=c.fetchall()
            if len(Data)==0:
                input("Empty")
                return
            Courses=[]
            for i in range (len(Data)):
                opj=Course()
                print("----------------------------------------------------------------")
                opj.Fill(Data[i])
                print(f"{i+1}-")
                opj.Viwe()
                print("----------------------------------------------------------------")
                Courses.append(opj)
            print(" select a Course")
            CourseID=Checker(1,len(Courses),1)
            if CourseID==-1:
                return
            else:
                while True:
                    ThisCourse=Courses[CourseID-1]
                    print(" 1- get OUT")
                    print(" 2- See Assignments")
                    print(" 3- See Students")
                    print(" 4- See Teachers")
                    print(" 5- Message The Professor ")
                    Choise=Checker(1,5,1)
                    if Choise==-1:
                        return
                    elif Choise==1:
                        ThisCourse.KickStudent(This.ID)
                        break
                    elif Choise==2:
                        while True:
                            Data =FetchFromData("Assignments","rowid,*" ,2,f"Course = {str(ThisCourse.ID)} ")
                            Assignments=[]
                            for i in range(len(Data)):
                                opj=Assignment()
                                opj.Fill(Data[i])
                                print("----------------------------------------------------------------")
                                print(f"{i+1}-")
                                opj.Viwe()
                                Assignments.append(opj)
                                print("----------------------------------------------------------------")
                            print(" Select a Assignment")
                            AssignmentID=Checker(1,len(Assignments),1)
                            if AssignmentID==-1:
                                break
                            else:
                                ThisAssignment=Assignments[AssignmentID-1]
                                This.SelectedAssignment(ThisAssignment)
                    elif Choise==3:
                        This.CourseStudents(ThisCourse)
                    elif Choise==4:
                        This.CourseTeachers(ThisCourse)
                    elif Choise==5:
                        This.CreateMessage(ThisCourse.CourseProf)
    
    def UI(This):
        while True:
            print(" 1- my Courses")
            print(" 2- register in a Course")
            print(" 3- InBox ")
            print(" 4- OutBox")
            print(" 5- logout ")
            print(" 6- Delete Account ")
            Choise=Checker(1,6,2)
            if Choise==1:
                This.MyCourses()
            elif Choise==2:
                while True:
                    sqript=f"""select rowid,* from Courses where not exists (select * from Registrations where Course = Courses.rowid and Student = {str(This.ID)}) """
                    c.execute(sqript)
                    Data=c.fetchall()
                    if len(Data)==0:
                        input("Empty")
                        break
                    Courses=[]
                    for i in range(len(Data)):
                        print("----------------------------------------------------------------")
                        print(f"{str(i+1)}-")
                        opj=Course()
                        opj.Fill(Data[i])
                        opj.Viwe()
                        Courses.append(opj)
                        print("----------------------------------------------------------------")
                    print(" select a COurse")
                    CourseID=Checker(1,len(Data),1)
                    if CourseID==-1:
                        break
                    else:
                        InsertIntoData("Registrations","Course,Student",f"{str(Courses[CourseID-1].ID)},{str(This.ID)} ")
                        input("Done")
                        break

            elif Choise==3:
                This.InBoX()
            elif Choise==4:
                This.OutBox()
            elif Choise==5:
                return
            elif Choise==6:
                This.Delete()
                return

class TeachingAssistants(User):

    def ShowInvitations(This):
        while True:
            Data=FetchFromData("Invitations","rowid,*",2,f"""TeachingAssistant = {str(This.ID)}""")
            if len(Data)==0:
                input("Empty")
                return
            Invitations=[]
            for i in range(len(Data)):
                opj=Invitation()
                opj.Fill(Data[i])
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-")
                opj.Viwe()
                print("----------------------------------------------------------------")
                Invitations.append(opj)
            print(" select an Invitation")
            InvitationID=Checker(1,len(Invitations),1)
            if InvitationID==-1:
                return
            else:
                ThisInvitation=Invitations[InvitationID-1]
                while True:
                    print(" 1- confirm")
                    print(" 2- cancle This Invitation")
                    print(" 3- Message This Professor")
                    Choise=Checker(1,3,1)
                    if Choise==-1:
                        break
                    elif Choise==1:
                        ThisInvitation.Confirm()
                        break
                    elif Choise==2:
                        ThisInvitation.Cancle()
                        break
                    elif Choise==3:
                        This.CreateMessage(ThisInvitation.FromWho)
                    
    def CourseTeachers(This,Course):
        while True:
            sqript=f""" select rowid,UserName from Users where exists (select * from Assistants Where Teacher = Users.rowid and Course={str(Course.ID)} ) and rowid != {str(This.ID)}; """
            c.execute(sqript)
            Teachers=c.fetchall()
            if len(Teachers)==0:
                input("only you")
                return
            for i in range(len(Teachers)):
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-\nUserName: {str(Teachers[i][1])}\n")
                print("----------------------------------------------------------------")
            print(" select a Teacher")
            ThisTeacher=Checker(1,len(Teachers),1)
            if ThisTeacher==-1:
                return
            else:
                while True:
                    print(" 1- Message ")
                    print(" 2- cancle")
                    Choise=Checker(1,2,3)
                    if Choise==1:
                        This.CreateMessage(Teachers[ThisTeacher-1][0])
                    elif Choise==2:
                        break
        
    def CourseStudents(This,Course):
        while True:
            sqript=f""" select rowid,UserName from Users where exists (select * from Registrations Where Student = Users.rowid and Course = {str(Course.ID)}); """
            c.execute(sqript)
            Students=c.fetchall()
            if len(Students)==0:
                input("Empty")
                return
            for i in range(len(Students)):
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-\nUserName: {str(Students[i][1])}\n")
                print("----------------------------------------------------------------")
            print(" select a Student")
            ThisStudent=Checker(1,len(Students),1)
            if ThisStudent==-1:
                return
            else:
                while True:
                    print(" 1- Message ")
                    print(" 2- cancle")
                    Choise=Checker(1,2,3)
                    if Choise==1:
                        This.CreateMessage(Students[ThisStudent-1][0])
                    elif Choise==2:
                        break

    def CourseAssignments(This,ThisCourse):
        while True:
            Data =FetchFromData("Assignments","rowid,*" ,2,f"Course = {str(ThisCourse.ID)} ")
            if len(Data)==0:
                input("Empty")
                return
            Assignments=[]
            for i in range(len(Data)):
                opj=Assignment()
                opj.Fill(Data[i])
                print("----------------------------------------------------------------")
                print(f"{str(i+1)}-")
                opj.Viwe()
                print("----------------------------------------------------------------")
                Assignments.append(opj)
            print(" select an Assignment")
            AssignmentID=Checker(1,len(Assignments),1)
            if AssignmentID==-1:
                return
            else:
                AssignmentID-=1
                while True:
                    ThisAssignment=Assignments[AssignmentID]
                    print(" 1- Graded Answers")
                    print(" 2- UnGraded Answers")
                    print(" 3- ExtraTime ")
                    Choise=Checker(1,3,1)
                    if Choise==-1:
                        break
                    elif Choise==1:
                        ThisAssignment.GradedAnswers(This)
                    elif Choise==2:
                        ThisAssignment.NotGradedAnswers(This)
                    elif Choise==3:
                        ThisAssignment.ExtraTime()

    def ShowCourses(This):
        while True:
            sqript=f"""select rowid,* from Courses where exists (select * from Assistants where Course = Courses.rowid and Teacher = {str(This.ID)} ); """
            c.execute(sqript)
            Data=c.fetchall()
            if len(Data)==0:
                input("Empty")
                return
            Courses=[]
            for i in range (len(Data)):
                print("----------------------------------------------------------------")
                opj=Course()
                opj.Fill(Data[i])
                opj.Viwe()
                print("----------------------------------------------------------------")
                Courses.append(opj)
            print(" select a Course")
            CourseID=Checker(1,len(Courses),1)
            if CourseID==-1:
                return
            else:
                ThisCourse=Courses[CourseID-1]
                while True:
                    print(" 1- Show Teachers")
                    print(" 2- Show Students")
                    print(" 3- SignOut Of The Course")
                    print(" 4- Message Professor")
                    print(" 5- Create Assignment")
                    print(" 6- Show Assignments ")
                    Choise=Checker(1,6,1)
                    if Choise==-1:
                        break
                    elif Choise ==1:
                        This.CourseTeachers(ThisCourse)
                    elif Choise ==2:
                        This.CourseStudents(ThisCourse)
                    elif Choise ==3:
                        ThisCourse.KickTeacher(This.ID)
                        break
                    elif Choise ==4:
                        This.CreateMessage(ThisCourse.CourseProf)
                    elif Choise ==5:
                        Ass=Assignment()
                        Ass.CreateAssignment(This.ID,ThisCourse.ID)
                    elif Choise ==6:
                        This.CourseAssignments(ThisCourse)

    def UI(This):
        while True:
            print(" 1- See Courses ")
            print(" 2- see Invitations ")
            print(" 3- see InBox")
            print(" 4- See OutBox")
            print(" 5- Logout")
            print(" 6- Delete Account")
            Choise=Checker(1,6,12)
            if Choise==5:
                return
            elif Choise== 6 :
                This.Delete()
                return
            elif Choise==4:
                This.OutBox()
            elif Choise==3:
                This.InBoX()
            elif Choise==2:
                This.ShowInvitations()
            elif Choise==1:
                This.ShowCourses()

class Invitation:
    ID=0
    Message=''
    FromWho=0
    FromName=''
    ToWho=0
    ToName=''
    ForCourse=0

    def Fill(This,Data):
        This.ID=Data[0]
        This.Message=Data[1]
        This.FromWho=Data[2]
        This.ForCourse=Data[3]
        This.ToWho=Data[4]
        This.FromName=FetchFromData("Users","UserName" ,1,f"rowid = {str(This.FromWho)}")[0]
        This.ToName=FetchFromData("Users","UserName" ,1,f"rowid = {str(This.ToWho)}")[0]
        
    def Viwe(This):
        print(f"From Professor: {str(This.FromName)}\nTo Teacher: {str(This.ToName)}\nFor Course: {str(This.ForCourse)}\nwith Message:\n{str(This.Message)}")

    def Cancle(This):
        sqript=f"""delete from Invitations where rowid = {str(This.ID)}"""
        c.execute(sqript)
        conn.commit()
    
    def Confirm(This):
        sqript=f"delete from Invitations where rowid ={This.ID}"
        c.execute(sqript)
        conn.commit()
        InsertIntoData("Assistants","Course, Teacher",f"{This.ForCourse},{This.ToWho}")