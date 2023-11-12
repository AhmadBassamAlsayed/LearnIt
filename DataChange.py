import sqlite3 as sql
conn =sql.connect("DataBase.dp")
c=conn.cursor()
def SetStudents():
    sqript="""
        create table if not exists Students (
        UserName varchar(50) unique,
        FullName varchar(75),
        PhoneNumber char(10),
        email varchar(50),
        age int
    );"""
    c.execute(sqript)
    conn.commit()

def SetProfessors():
    sqript="""
        create table if not exists Professors(
        UserName varchar(50) unique,
        FullName varchar(75),
        PhoneNumber char(10),
        email varchar(50),
        age int
    );"""
    c.execute(sqript)
    conn.commit()

def SetTeachingAssistants():
    sqript="""
        create table if not exists TeachingAssistants(
        UserName varchar(50) unique,
        FullName varchar(75),
        PhoneNumber char(10),
        email varchar(50),
        age int
    );"""
    c.execute(sqript)
    conn.commit()

def SetCourses():
    sqript="""create table if not exists Courses(
        Name varchar(50),
        Description text,
        CourseProf int,
        foreign key (CourseProf) references Professors(rowid) on delete cascade 
    );"""
    c.execute(sqript)
    conn.commit()

def SetInvitations():
    sqript="""
        create table if not exists Invitations(
        Massege text,
        Prof int,
        Course int ,
        TeachingAssistant int,
        foreign key (Prof) references Professors(rowid) on delete cascade ,
        foreign key (Course) references Courses(rowid) on delete cascade ,
        foreign key (TeachingAssistant) references TeachingAssistants(rowid) on delete cascade 
        );"""
    c.execute(sqript)
    conn.commit()

def SetAssistants():
    sqript="""
        create table if not exists Assistants(
        Course int,
        Prof int,
        foreign key (Course) references Courses(rowid) on delete cascade,
        foreign key (Prof) references TeachingAssistants(rowid) on delete cascade
        );"""
    c.execute(sqript)
    conn.commit()
    
def SetRegistrations():
    sqript="""
        create table if not exists Registrations(
        Student int,
        Course int,
        foreign key (Student) references Students(rowid) on delete cascade,
        foreign key (Course) references Courses(rowid) on delete cascade
        );"""
    c.execute(sqript)
    conn.commit()

def SetAssignments():
    sqript="""
        create table if not exists Assignments(
        Course int ,
        Prof int ,
        Assistant int ,
        foreign key (Course) references Courses(rowid) on delete cascade,
        foreign key (Prof) references Professors(rowid) on delete cascade ,
        foreign key (Assistant) references TeachingAssistants(rowid) on delete cascade 
        );"""
    c.execute(sqript)
    conn.commit()
    
def SetAnswers():
    sqript="""
        create table if not exists Answers(
        Answer text,
        Student int ,
        Assignment int,
        foreign key (Student) references Students(rowid) on delete cascade,
        foreign key (Assignment) references Assignments(rowid) on delete cascade
        );"""
    c.execute(sqript)
    conn.commit()
    

def SetDataBase():

    SetStudents()
    SetProfessors()
    SetTeachingAssistants()  
    SetCourses()
    SetInvitations()
    SetAssistants()
    SetRegistrations()
    SetAssignments()
    SetAnswers()