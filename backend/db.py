'''
Defines helper functions used in API calls using pyodbc (for database connections)
and SQL prepared statements
'''
import pyodbc

# connection information can change as we include security

conn = (r'Driver=SQL Server;'
        r'Server=(local);'
        r'Database=StudyBuddy;'
        r'username=SA;'
        r'password=dbtools.IO'
        )
cnxn = pyodbc.connect(conn)
cursor = cnxn.cursor()

'''
PRECONDITION: passed string <username> which will be used to find the user in the db
POSTCONDITION: if the user with <username> exists in the database, return their information (form of string)
'''


def getUser(name):
    result = cursor.execute("SELECT * FROM Users WHERE username = ?", name).fetchone()
    return result


'''
PRECONDITION: account creation requested, need to add a new entry to users table
POSTCONDITION: account has been created and added to users table with given information
'''


def createAccount(username, password):
    # cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)",username, password)
    prep_stmt = "INSERT INTO Users (username, password) VALUES (?,?)"
    cursor.execute(prep_stmt, username, password)


''' 
PRECONDITION: all users are present in the db
POSTCONDITION: user with 'username' has been removed from the db
'''


def removeUser(username):
    cursor.execute("DELETE FROM Users WHERE username = ?", username)


'''
PRECONDITION: no users have been retrieved
POSTCONDITION: formatted records of all users returned
'''

'''def getAllUsers():
    temp = cursor.execute("SELECT * FROM Users")
    for [uID, username, password, user_email, xp] in temp:
        result = str(uID) + " " + str(username) + " " + str(password) + " " + str(user_email) + " " + str(xp)
    return result
'''

# Class Methods
'''
PRECONDITION: no classes have been retrieved from db
POSTCONDITION: all classes for user 'username' have been retrieved (if the class is uncomplete)
'''


def getClasses(username):
    # get user id
    userID = getUser(username).uID
    # count all records
    # count = cursor.execute("SELECT COUNT(*) FROM Classes WHERE FK_uID = ? ")
    record = cursor.execute("SELECT * FROM Classes WHERE FK_uID = ? AND is_complete = 0", userID).fetchall()
    return record


'''
PRECONDITION: class id for individuals unknown
POSTCONDITION: returns classID for specified user and specified class
'''


def getClassID(username, className):
    userID = getUser(username).uID
    record = cursor.execute("SELECT cID FROM Classes WHERE FK_uID = ? AND class_Name =? ", userID, className).fetchone()
    return record.cID


'''
PRECONDITION: no classes retrieved
POSTCONDITION: a single class is returned when given username and class id
'''


def getSingleClass(username, className):
    userID = getUser(username).uID
    classID = getClassID(username, className)
    return cursor.execute("SELECT * FROM Classes WHERE FK_uID = ? AND cID = ?", userID, classID).fetchone()


# returns the record of the class added
def addClass(username, className, timeslot):
    prep_stmt = "INSERT INTO Classes (class_Name, timeslot, FK_uID) VALUES (?,?,?)"
    id = getUser(username).uID
    return cursor.execute(prep_stmt, className, timeslot, id)


def removeClass(username, className):
    id = getUser(username).uID
    classID = getClassID(username, className)
    record = cursor.execute("DELETE FROM Classes WHERE FK_uID = ? AND cID = ?", id, classID)
    return record


'''
PRECONDITION: all classes marked uncomplete
POSTCONDITION: specified class marked complete
'''


# returns record of newly completed class - doesnt remove class from db
def completeClass(username, className):
    classID = getClassID(username, className)
    userID = getUser(username).uID
    record = cursor.execute("UPDATE Classes SET is_complete = ? WHERE cID = ? AND FK_uID = ?", 1, classID,
                            userID).fetchone()
    return record


def addClassMeta():
    return


'''
PRECONDITION: the total study time for the class is unchanged
POSTCONDITION: total study time for the specified class for the specified user has been updated with time studied
'''


# studyTime is currently a float, will have to change this
def addStudyTime(username, className, t):
    userID = getUser(username).uID
    record = getSingleClass(username, className)
    classID = record.cID
    # print(record.studyTime)
    uTime = record.studyTime + t
    return cursor.execute("UPDATE Classes SET studyTime = ? WHERE FK_uID = ? AND cID = ?", uTime, userID, classID).fetchone()


# Tasks
''''
PRECONDITION: no tasks have been retrieved
POSTCONDITION: list of tasks per class retrieved
'''


def getTaskList(username, className):
    userID = getUser(username).uID
    classID = getClassID(className)
    return cursor.execute("SELECT * FROM Tasks WHERE FK_uID = ? AND FK_cID = ?", userID, classID).fetchall()


def getTaskID(username, className, taskName):
    userID = getUser(username).uID
    classID = getClassID(className)
    record = cursor.execute("SELECT * FROM Tasks WHERE FK_uID = ? AND FK_cID = ? AND task_Name = ?", userID, classID,
                            taskName)
    return record.tID


def completeTask(username, className, taskName, grade):
    taskID = getTaskID(username, className, taskName)
    userID = getUser(username).uID
    classID = getClassID()
    return cursor.execute("UPDATE Tasks SET task_grade = ? WHERE FK_uID = ? AND FK_cID = ? AND tID = ?", grade, userID,
                          classID, taskID)
