from tinydb import TinyDB, Query
from datetime import datetime
import os
import subprocess

dir_path = os.path.dirname(os.path.abspath(__file__))
db_path = dir_path #+ '/db/'

class studentDB:
    def __init__(self, fname="/students.json"):
        self.db = TinyDB(db_path+fname)
        print("DB file:", db_path+fname)
        
    def add_student(self, studentName):
        print(" inserting ", studentName)
        id = self.db.insert({
            'studentName': studentName,
            'sessions': {
                "Monday_AM": "",
                "Monday_PM": "",
                "Tuesday_AM": "",
                "Tuesday_PM": "",
                "Wednesday_AM": "",
                "Wednesday_PM": "",
                "Thursday_AM": "",
                "Thursday_PM": "",
                "Friday_AM": "",
                "Friday_PM": ""
            }
            
            }
        )


        print(" upserting ", studentName)
        Stu = Query()
        id = self.db.upsert({
            'id': id,
            'studentName': studentName
            
        }, Stu.studentName == studentName)

    def getStudents(self):
        return self.db.all()
    
    def updateStudentSession(self, student, session, dayTime):
        Stu = Query()
        
        info = self.getStudent(student)[0]
        print("info:", info)
        ses = info["sessions"]
        ses[dayTime] = session

        id = self.db.upsert({
            'sessions': ses

        }, Stu.studentName == student)

        return id
    
    def getStudent(self, student):
        Stu = Query()
        info = self.db.search(Stu.studentName == student)
        print(info)
        return info



class sessionDB:
    def __init__(self, fname="/sessions.json"):
        self.db = TinyDB(db_path+fname)
        print("DB file:", db_path+fname)
        
    def add_session(self, sessionName, faculty="", studentLead="", location=""):
        print(" inserting ", sessionName)
        id = self.db.insert({
                'sessionName': sessionName,
                'faculty': faculty,
                'studentLead': studentLead,
                'location': location
            }
        )


        print(" upserting ", sessionName)
        Q = Query()
        id = self.db.upsert({
            'id': id,
        }, Q.sessionName == sessionName)

    def getAll(self):
        return self.db.all()
    
    def close(self):
        self.db.close()


class sessionCollator:
    def __init__(self):
        print("student db:", db_path+'/students.json')
        s = studentDB()
        self.students = s.getStudents()
        s = sessionDB()
        self.sessions = s.getAll()

    def collate(self):

        dayTimes = ["Monday_AM", "Monday_PM", "Tuesday_AM", "Tuesday_PM", "Wednesday_AM", "Wednesday_PM", "Thursday_AM", "Thursday_PM", "Friday_AM", "Friday_PM"]

        print("students", self.students)
        print()
        print("sessions", self.sessions)

        assignments = {}

        
        for session in self.sessions:
            sesTime = session['sessionName'] + "@"
            for dayTime in dayTimes:
                sesTime = session['sessionName'] + "@" + dayTime
                assignments[sesTime] = []
                for student in self.students:
                    if student["sessions"][dayTime] == session['sessionName']:
                        assignments[sesTime].append(student['studentName'])

        print()
        print("assignments:")
        for assignment in assignments:
            print(assignment, assignments[assignment])

        return assignments





def setupStudents():
    db = studentDB()

    with open("names.txt") as f:
        students = f.readlines()
    #students = ["Millie", "Danny", "Aiden"]
    for student in students:
        student=student.strip()
        db.add_student(student)
        print(student)


def setupSessions():
    db = sessionDB()
    with open("sessions.txt") as f:
        sessions = f.readlines()
    # sessions = ["Makerspace", "Cooking", "Field Trips", "College Visits"]
    for session in sessions[1:]:
        print("session:", session)
        data = session.split(",")
        print("data:", data)
        if (len(data) >= 4):
            ses = data[0].strip()
            faculty = data[1].strip()
            studentLead = data[2].strip()
            location = data[3].strip()
            db.add_session(ses, faculty, studentLead, location)


if __name__ == '__main__':
    #setup
    setupStudents()
    setupSessions()

        
