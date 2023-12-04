import sqlite3 as sql
conn =sql.connect("DataBase.dp")
c=conn.cursor()
def SetUsers():
    sqript="""
        create table if not exists Users (
        UserName varchar(50) unique,
        FullName varchar(75),
        Email varchar(50) unique,
        Password varchar(50),
        Position char(1)
    );"""
    c.execute(sqript)
    conn.commit()

def SetMessages():
    sqript="""create table if not exists Messages(
        FromWho int,
        ToWho int,
        Message text,
        foreign key (FromWho) references Users(rowid) on delete cascade 
        foreign key (ToWho) references Users(rowid) on delete cascade 
    );"""
    c.execute(sqript)
    conn.commit()

def SetCourses():
    sqript="""create table if not exists Courses(
        Name varchar(50),   
        Description text,
        CourseProf int,
        foreign key (CourseProf) references Users(rowid) on delete set null 
    );"""
    c.execute(sqript)
    conn.commit()

def SetInvitations():
    sqript="""
        create table if not exists Invitations(
        Message text,
        Professor int,
        Course int ,
        TeachingAssistant int,
        foreign key (Professor) references Users(rowid) on delete cascade ,
        foreign key (Course) references Courses(rowid) on delete cascade ,
        foreign key (TeachingAssistant) references Users(rowid) on delete cascade 
        );"""
    c.execute(sqript)
    conn.commit()

def SetAssistants():
    sqript="""
        create table if not exists Assistants(
        Course int,
        Teacher int,
        foreign key (Course) references Courses(rowid) on delete set null,
        foreign key (Teacher) references Users(rowid) on delete cascade
        );"""
    c.execute(sqript)
    conn.commit()
    
def SetRegistrations():
    sqript="""
        create table if not exists Registrations(
        Student int,
        Course int,
        foreign key (Student) references Users(rowid) on delete cascade,
        foreign key (Course) references Courses(rowid) on delete cascade
        );"""
    c.execute(sqript)
    conn.commit()

def SetAssignments():
    sqript="""
        create table if not exists Assignments(
        Assignment text,
        Course int,
        Creater int,
        StartDate varchar(30),
        EndDate varchar(30),
        foreign key (Course) references Courses(rowid) on delete cascade,
        foreign key (Creater) references Users(rowid) on delete set null 
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
        SubmitDate varchar(30),
        Grade decimal default null,
        GradeMessage Text default null,
        foreign key (Student) references Users(rowid) on delete cascade,
        foreign key (Registration) references Registrations(rowid) on delete cascade,
        foreign key (Assignment) references Assignments(rowid) on delete cascade
        );"""
    c.execute(sqript)
    conn.commit()

def SetDataBase():

    # print("-----------------")
    SetUsers()
    SetCourses()
    SetInvitations()
    SetAssistants()
    SetRegistrations()
    SetAssignments()
    SetAnswers()
    SetMessages()