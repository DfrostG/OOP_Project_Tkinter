class User:
    def __init__(self, username, password, email, fname, lname, gender, birth_date, education, province, country,
                 user_type):
        self.__username = username
        self.__password = password
        self.__email = email
        self.__fname = fname
        self.__lname = lname
        self.__gender = gender
        self.__birth_date = birth_date
        self.__education = education
        self.__province = province
        self.__country = country
        self.__user_type = user_type
        
    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_fname(self):
        return self.__fname

    def get_lname(self):
        return self.__lname

    def get_gender(self):
        return self.__gender

    def get_birth_date(self):
        return self.__birth_date

    def get_education(self):
        return self.__education

    def get_province(self):
        return self.__province

    def get_country(self):
        return self.__country

    def get_user_type(self):
        return self.__user_type
        
        
class Admin(User):
    def __init__(self, username, password, email, fname, lname, gender, birth_date, education, province, country):
        User.__init__(self, username, password, email, fname, lname, gender, birth_date, education, province,
                      country, user_type="Admin")


class Student(User):
    def __init__(self, username, password, email, fname, lname, gender, birth_date, education, province, country):
        User.__init__(self, username, password, email, fname, lname, gender, birth_date, education, province, country,
                      user_type="Student")
        self._enrolled_course = []       
    
    def get_enrolled_course(self):
        return self._enrolled_course

    def set_enrolled_course(self, request, will_enroll):
        if request == 'enroll':
            self._enrolled_course.append(will_enroll)
        elif request == 'unenroll':
            self._enrolled_course.remove(will_enroll)
            
    def enroll_course(self, course):
        self._enrolled_course.append(course)
                

class Teacher(User):
    def __init__(self, username, password, email, fname, lname, gender, birth_date, education,
                 province, country, teacher_dept):
        User.__init__(self, username, password, email, fname, lname, gender, birth_date, education, province, country,
                      user_type="Teacher")
        self.__teacher_dept = teacher_dept
        self.__teached = []
