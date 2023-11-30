import sqlite3 as sql
import datetime
conn =sql.connect("DataBase.dp")
c=conn.cursor()

def JoinTables(TableA,TableB,FromTableA,FromTableB,MatchFromA,MachFromB,OneOrAll):
    sqript=f"""SELECT {TableA}.{FromTableA}, {TableB}.{FromTableB} FROM {TableA} INNER JOIN {TableB} ON {TableA}.{MatchFromA} = {TableB}.{MachFromB}"""
    c.execute(sqript)
    Data=[]
    if OneOrAll==1:
        Data=c.fetchone()
    else:
        Data=c.fetchall()
    return Data



def FetchFromData(Table,Atributes,OneOrAll,Where):
    sqript=f"""select {Atributes} from {Table} where {Where}"""
    c.execute(sqript)
    Data=0
    if OneOrAll==1:
        Data=c.fetchone()
    else:
        Data=c.fetchall()
    return Data

def InsertIntoData(Table,Atriputes,Values):
    sqript=f"""insert into {Table} ({Atriputes}) values ({Values})"""
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
        num=input(f'Enter a number [{num1},{num2}]{c1}:\n')
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

    def InBoX(This):
        while True:
            Data=FetchFromData("Messages","rowid,*",2,f"ToWho = {This.ID} ")
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
                    print(f"{i+1}-\n")
                    Messages[i].Viwe()
                # select a Message
                ThisMessage=Checker(1,len(Messages),1)
                if ThisMessage==-1:
                    return
                else:
                    MessageIndex=ThisMessage-1
                    while True:
                        # 1- delete
                        # 2- Message The Sender
                        Choise=Checker(1,2,1)
                        if Choise==-1:
                            break
                        elif Choise==1:
                            Messages[MessageIndex].Delete()
                        elif Choise==2:
                            This.CreateMessage(Messages[MessageIndex].FromWho)

    def OutBox(This):
        while True:
            Data=FetchFromData("Messages","rowid,*",2,f"FromWho = {This.ID} ")
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
                    print(f"{i+1}-\n")
                    Messages[i].Viwe()
                # select a Message
                ThisMessage=Checker(1,len(Messages),1)
                if ThisMessage==-1:
                    return
                else:
                    MessageIndex=ThisMessage-1
                    while True:
                        # 1- delete
                        # 2- Message The Reciver
                        Choise=Checker(1,2,1)
                        if Choise==-1:
                            break
                        elif Choise==1:
                            Messages[MessageIndex].Delete()
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
        InsertIntoData("Messages"," FrommWho, ToWho, Message",f"""{This.ID},{To},"{Text}" """)
        
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
        cur=FetchFromData("Users","UserName,Position",1,f"rowid = {This.FromWho}")
        This.FromName=cur[0]
        This.FromType=cur[1]
        This.ToWho=Data[2]
        cur=FetchFromData("Users","UserName,Position",1,f"rowid = {This.ToWho}")
        This.ToName=cur[0]
        if cur[1]=='T':
            This.ToType="Teacher"
        if cur[1]=='P':
            This.ToType="Professor"
        if cur[1]=='S':
            This.ToType="Student"
        This.Text=Data[3]
    
    def Delete(This):
        sqript=f"""delete from Messages where rowid = {This.ID}"""
        c.execute(sqript)
        conn.commit()

    def Viwe(This):
        print(f"From {This.FromType}: {This.FromName}\nTo {This.ToType}: {This.ToName}\n{This.Text}\n")

class Professor(User):

    def CreateCourse(This):
        Name=input("Enter The Cousre Name:")
        Discription=input("Enter The Course Discription:")
        # 1- confirm the creation
        # 2- cnacle  
        Choise=Checker(1,2,2)
        if Choise==1:
            InsertIntoData("Courses","Name, Description, CourseProf ",f""" "{Name}", "{Discription}",{This.ID} """)
        else:
            return
    
    def CreateInvite(This,Course):
        AvTeachers=[]
        sqript=f"""select rowid,UserName from Users where Position = "T" and not exists (select * from Invitations where TeachingAssistant = User.rowid)"""
        c.execute(sqript)
        AvTeachers=c.fetchall()
        for i in range(len(AvTeachers)):
            print("----------------------------------------------------------------")
            print(f"{i+1}-\n\t{AvTeachers[i][1]}")
            print("----------------------------------------------------------------")
        if len(AvTeachers)==0:
            input("Empty")
            return
        # select a teacher
        Teacher=Checker(1,len(AvTeachers),1)
        if Teacher==-1:
            return
        else:
            TeacherID=AvTeachers[Teacher-1][0]
            Message=input("type a message dont let it empty:")
            if Message=='':
                Message ='Empty Message!'
            InsertIntoData("Invitations","Message, Professor, Course, TeachingAssistant",f""" "{Message}", {This.ID},{Course.ID},{TeacherID} """)
            # Done
            return
    
    def SelectedStudent(This,Course,StudentID):
        while True:
            # 1- kick
            # 2- Message 
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
            sqript =f""""select rowid,UserName from Users where exists (select * from Registration where Student = Users.rowid and Course ={Course.ID} );"""
            c.execute(sqript)
            AvStudents=c.fetchall()
            for i in range(len(AvStudents)):
                print("----------------------------------------------------------------")
                print(f"{i+1}-\n\t{AvStudents[i][1]}")
                print("----------------------------------------------------------------")
            if len(AvStudents)==0:
                input("Empty")
                return
            # select a Student
            Student=Checker(1,len(AvStudents),1)
            if Student==-1:
                return
            else:
                StudentID=AvStudents[Student-1][0]
                This.SelectedStudent(Course,StudentID)

    def SelectedTeacher(This,Course,TeacherID):
        # 1- message him 
        # 2- kick him From This Course
        Choise=Checker(1,2,1)
        if Choise==-1:
            return
        elif Choise==1:
            This.CreateMessage(TeacherID)
        elif Choise==2:
            Course.KickTeacher(TeacherID)

    def ShowTeachers(This,Course):
        while True:    
            sqript=f"""select rowid,UserName from Users where exists (select * from Assistants Where Teacher = Users.rowid and Course={Course.ID})"""
            c.execute(sqript)
            Teachers=c.fetchall()
            if len(Teachers)==0:
                print 
            for i in range(len(Teachers)):
                print("----------------------------------------------------------------")
                print(f"{i+1}-\n\t{Teachers[i][1]}")
                print("----------------------------------------------------------------")
            # select a Teacher 
            Teacher=Checker(1,len(Teachers),1)
            if Teacher==-1:
                return
            else:
                TeacherID=Teacher-1
                This.SelectedTeacher(Course,TeacherID)

    def SelectedAssignment(This,AssignmentID):
        while True:
            # 1- UnGraded Answers
            # 2- Greded Aswers
            # 3- delete 
            Choise=Checker(1,3,1)
            ThisAssignment=Assignment()
            ThisAssignment.Fill(FetchFromData("Assignments","rowid,*",1,f"""rowid = {AssignmentID}"""))
            if Choise==-1:
                return
            elif Choise==1:
                ThisAssignment.NotGradedAnswers(This)
            elif Choise==2:
                ThisAssignment.GradedAnswers(This)
            elif Choise==3:
                # Are you sure ?
                # 1- Yes
                # 2- cancle 
                Choise=Checker(1,2,3)
                if Choise==1:
                    ThisAssignment.Delete()
                else:
                    continue

    def ShowAssignments(This,Course):
        while True:
            Data=Course.Assignments()
            if len(Data)==0:
                input("Empty")
                return
            else:
                Assignments=[]
                for i in range(Data):
                    opj=Assignment()
                    opj.Fill(Data[i])
                    Assignments.append(opj)
                for i in range(len(Assignments)):
                    print ("----------------------------------------------------------------")
                    print(f"{i+1}-\n")
                    Assignments[i].Viwe()
                    print ("----------------------------------------------------------------")
                    # select an Assignment
                    Assignment=Checker(1,len(Assignments),1)
                    if Assignment==-1:
                        return
                    else:
                        AssignmentID=Assignment-1
                        This.SelectedAssignment(AssignmentID)

    def SelectedCourse(This,Course):
        while True:
            # 1- send invite
            # 2- Show Students
            # 3- Show Teachers
            # 4- Show Assignments
            # 5- Add Assignment
            # 6- Delete Course
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
                # Are You Sure?
                # 1- yes 
                # 2- no
                Choise=Checker(1,2,3)
                if Choise==1:
                    Course.Delete()

    def SeeCourses(This):
        while True:
            Data=FetchFromData("Courses","rowid,*",2,f"CourseProf = {This.ID}")
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
                print(f"{i+1}-")
                Courses[i].Viwe()
                print("----------------------------------------------------------------")
            # select a course
            Choise=Checker(1,len(Courses),1)
            if Choise==-1:
                return
            else:
                This.SelectedCourse(Courses[i-1])

    def ShowInvitations(This):
        while True:
            Data=FetchFromData("Invitations" ,"rowid,*",2,f"Professor = {This.ID}")
            if len(Data)==0:
                input("Empty")
                return
            else:
                Invitations=[]
                for i in range(Data):
                    opj=Invitation()
                    opj.Fill(Data[i])
                    print("----------------------------------------------------------------")
                    print(f"{i+1}-\n")
                    opj.Viwe()
                    print("----------------------------------------------------------------")
                # select an Invitation
                ThisInvitation=Checker(1,len(Invitations),1)
                if ThisInvitation==-1:
                    return
                else:
                    ThisInvitation=Invitations[ThisInvitation-1]
                    while True:
                        # 1- Message The Teacher
                        # 2- cancle The invitation
                        Choise=Checker(1,2,1)
                        if Choise==-1: 
                            break
                        elif Choise==1:
                            This.CreateMessage(ThisInvitation.ToWho)
                        elif Choise==2:
                            # are you sure
                            # 1- yes
                            # 2- no 
                            Cancle=Checker(1,2,3)
                            if Cancle==1:
                                ThisInvitation.Cancle()
    
    def UI(This):
        while True:
            # what you want to do 
            # 1- see courses and maneg them
            # 2- invites 
            # 3- create a course 
            # 4- Inbox
            # 5- OutBox 
            # 6- loge out
            To =Checker(1,4,2)
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
            
class Answer:
    ID=0
    Text=''
    Student=0 
    Assignment=0
    Registration=0
    SubmitDate=0
    Grade=-1
    StudentName=0
    GradeMessage=''

    def Fill(This,Data):
        This.ID=Data[0]
        This.Text=Data[1]
        This.Student=Data[2] 
        This.Assignment=Data[3]
        This.Registration=Data[4]
        This.SubmitDate=datetime.datetime.strptime(Data[5],"%d-%m-%Y")
        This.Grade=Data[6]
        This.GradeMessage=Data[7]
        This.StudentName=FetchFromData("Users"," UserName ",1,f"""rowid = {This.Student}""")
    
    def Viwe(This):
        print(f"From: {This.StudentName}\nDate: {This.SubmitDate}\nAnswer:\n{This.Text}")
        if This.Grade==-1:
            print("Not Graded")
        else:
            print(f"Grade: {This.Grade}/10")
    
    def MakeGrade(This):
        # Enter The grade
        Grade=Checker(0,10,1)
        if Grade==-1:
            return
        else:
            This.Grade=Grade
            sqript=f"""update Answers set Grade = {This.Grade} WHERE rowid = {This.ID};"""
            c.execute(sqript)
            conn.commit()
    # def CreateAnswer(This,AssignmentID):
    def NotGraded(This,User):
        while True:
            # 1- Grade
            # 2- Message Student
            Choise=Checker(1,2,1)
            if Choise==-1:
                return
            elif Choise==1:
                This.MakeGrade()
            elif Choise==2:
                User.CreateMessage(This.Student)
    
    def Graded(This,User):
        while True:
            # 1- ChangeGrade
            # 2- Message Student
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
    FromName=''
    FromCourse=0
    
    def Fill(This,Data):
        This.ID=Data[0]
        This.Text=Data[1]
        This.FromCourse=Data[2]
        This.FromID=Data[3]
        This.StartDate=datetime.datetime.strptime(Data[4],"%d-%m-%Y")
        This.EndDate=datetime.datetime.strptime(Data[5],"%d-%m-%Y")
        # datetime_obj = datetime.datetime.strptime(date_string, date_format)
        This.FromName=FetchFromData("Users"," UserName ",1,f"""rowid = {This.FromID}""")

    def CreateAssignment(This,FromID,FromCourse):
        Text=input("Enter The Assignment and Press \'Enter\' to conferm it and DONT USE (\") :\n")
        StartDate=datetime.datetime.now()
        StartDate=StartDate.strptime('%d-%m-%y')
        EndDate=StartDate
        while StartDate<=EndDate:
            Date=input("Enter The end date in format (DD-MM-YYYY) and it has to be at les tommorow")
            try:
                EndDate=StartDate.strftime('%D-%m-%y')
            except:
                continue
        sqript=f"""insert into Assignments (Assignment,Course,Creater,StartDate,EndDate) values ("{Text}",{FromCourse},{FromID},"{StartDate}","{EndDate}")"""
        c.execute(sqript)
        conn.commit()
    
    def Viwe(This):
        print(f"Creater: {This.FromName}\nStartDate: {This.StartDate}\nEndDate: {This.EndDate}\n{This.Text}\n")

    def NotGradedAnswers(This,User):
        Data=FetchFromData("Answers"," rowid,* ",2,f"""Assignment = {This.ID} and SubmitDate != "00-00-0000" and Greade = Null """ )
        Answers=[]
        if len(Data)==0:
            input("Empty")
            return
        for i in Data:
            opj=Answer()
            opj.Fill(i)
            Answers.append(opj)
            print ("----------------------------------------------------------------")
            opj.Viwe()
            print ("----------------------------------------------------------------")
        # select an Answer
        Answer=Checker(1,len(Answers),1)
        if Answer==-1:
            return
        else:
            AnswerID=Answer-1
            Answers[AnswerID].NotGraded(User)
        
    def GradedAnswers(This,User):
        Data=FetchFromData("Answers"," rowid,* ",2,f"""Assignment = {This.ID} and SubmitDate != "00-00-0000" and Greade != Null """ )
        Answers=[]
        if len(Data)==0:
            input("Empty")
            return
        for i in Data:
            opj=Answer()
            opj.Fill(i)
            Answers.append(opj)
            print ("----------------------------------------------------------------")
            opj.Viwe()
            print ("----------------------------------------------------------------")
        # select an Answer
        Answer=Checker(1,len(Answers),1)
        if Answer==-1:
            return
        else:
            AnswerID=Answer-1
            Answers[AnswerID].Graded(User)
                

    def Delete(This):
        sqript=f"delete from Assignments where rowid = {This.ID}"
        c.execute(sqript)
        conn.commit()
        sqript=f"""delete from Answers Where Assignment ={This.ID} """
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
    
    def Assignments(This):
        return FetchFromData("Assignments","rowid,*" ,2,f"Course = {This.ID} ")

# class Student(User):

# class TeachingAssistants(User):

class Invitation:
    ID=0
    Message=''
    FromWho=0
    ToWho=0
    ForCourse=0
    FromName=''
    ToName=''

    def Fill(This,Data):
        This.ID=Data[0]
        This.Message=Data[1]
        This.FromWho=Data[2]
        This.ForCourse=Data[3]
        This.ToWho=Data[4]
        
        sqript=f"select UserName from Users where rowid = {This.FromWho}"
        c.execute(sqript)
        This.FromName=c.fetchone()
        
        sqript=f"select UserName from Users where rowid = {This.ToWho}"
        c.execute(sqript)
        This.ToName=c.fetchone()

    def Viwe(This):
        print(f"From Professor: {This.FromName}\nFor Course: {This.ForCourse}\nwith Message:\n{This.Message}")


    def Cancle(This):
        sqript=f"""delete from Invitations where rowid = {This.ID}"""
        c.execute(sqript)
        conn.commit()
    
    # def Confirm(This):

