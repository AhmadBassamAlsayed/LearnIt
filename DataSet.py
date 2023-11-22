import sqlite3 as sql
conn =sql.connect("DataBase.dp")
c=conn.cursor()
def SetStudents():
    sqript="""
        create table if not exists Students (
        UserName varchar(50) unique,
        FullName varchar(75),
        PhoneNumber char(10) unique,
        Email varchar(50) unique,
        Password varchar(50)
    );"""
    c.execute(sqript)
    conn.commit()
    
def SetProfessors():
    sqript="""
        create table if not exists Professors(
        UserName varchar(50) unique,
        FullName varchar(75),
        PhoneNumber char(10) unique,
        Email varchar(50) unique,
        Password varchar(50)
    );"""
    c.execute(sqript)
    conn.commit()

def SetTeachingAssistants():
    sqript="""
        create table if not exists TeachingAssistants(
        UserName varchar(50) unique,
        FullName varchar(75),
        PhoneNumber char(10) unique,
        Email varchar(50) unique,
        Password varchar(50)
    );"""
    c.execute(sqript)
    conn.commit()

def SetCourses():
    sqript="""create table if not exists Courses(
        Name varchar(50),   
        Description text,
        CourseProf int,
        foreign key (CourseProf) references Professors(rowid) on delete set null 
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
        Teacher int,
        foreign key (Course) references Courses(rowid) on delete set null,
        foreign key (Teacher) references TeachingAssistants(rowid) on delete cascade
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
        Assignment text,
        Course int,
        Prof int,
        Assistant int ,
        StartDate vatchar(10),
        EndDate varchar(10),
        foreign key (Course) references Courses(rowid) on delete cascade,
        foreign key (Prof) references Professors(rowid) on delete set null ,
        foreign key (Assistant) references TeachingAssistants(rowid) on delete set null
        );"""
    c.execute(sqript)
    conn.commit()
    
def SetAnswers():
    sqript="""
        create table if not exists Answers(
        Answer text,
        Student int,
        Assignment int,
        Registration int,
        Date vatchar(10),
        Grade decimal defult null, 
        foreign key (Student) references Students(rowid) on delete cascade,
        foreign key (Registration) references Registrations(rowid) on delete cascade,
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