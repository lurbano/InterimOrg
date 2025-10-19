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



class sessionDB:
    def __init__(self, fname="/sessions.json"):
        self.db = TinyDB(db_path+fname)
        print("DB file:", db_path+fname)
        
    def add_session(self, sessionName, faculty="", location=""):
        print(" inserting ", sessionName)
        id = self.db.insert({
                'sessionName': sessionName,
                'faculty': faculty,
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
    sessions = ["Makerspace", "Cooking", "Field Trips", "College Visits"]
    for session in sessions:
        db.add_session(session)


if __name__ == '__main__':
    #setup
    setupStudents()
    setupSessions()

        
