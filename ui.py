import tkinter.messagebox
from tkinter import *
from login import *
from course import *
from user import *

class CourseUI:
    def __init__(self, username, user_type):
        self._username = username
        self._user_type = user_type
        self.__font = 'Helvetica'
        self.__normal_size = 16
        self._window = Tk()
        self._window.title("CE MOOC")
        self._window.geometry('600x600+0+0')
        self.__is_cart_open = False

        # --------------------------------- Menu --------------------------------- #
        menu = Menu()
        menu_item = Menu()
        if self._user_type in ["User", "Teacher"]:
            menu_item.add_command(label='Edit Profile', command=self.editprofile)
            menu_item.add_command(label='My Course', command=self.mycourse)
        if self._user_type == "Admin":
            menu_item.add_command(label='Admin Portal', command=self.adminportal)
        if self._user_type == "Guest":
            menu_item.add_command(label='Register', command=self.register)
        menu_item.add_command(label='Logout', command=self.logout)
        self._window.config(menu=menu)
        menu.add_cascade(label="Your account: "+self._username, menu=menu_item)
        menu.add_cascade(label="About")

        # --------------------------------- Course List --------------------------------- #
        Label(self._window, text="All Courses", font=(self.__font, 18, 'bold')).grid(row=0, column=2)
        cl = CourseCatalog().get_course_catalog()
        for i in range(len(cl)):
            Label(self._window, text=cl[i][0]+": ", font=(self.__font, self.__normal_size)).grid(row=i+1, column=1)
            Label(self._window, text=cl[i][1], font=(self.__font, self.__normal_size)).grid(row=i+1, column=2)
            Button(self._window, text="View", font=(self.__font, self.__normal_size)).grid(row=i+1, column=4)
            if self._user_type not in ["Guest", "Admin"]:
                Button(self._window, text="Enroll", font=(self.__font, self.__normal_size), command=self.cart).grid(row=i+1, column=3)

        self._window.mainloop()
    def logout(self):
        self._window.destroy()
        LoginUI()
    def cart(self):
        print(self.__is_cart_open)
        if not self.__is_cart_open:
            self.__is_cart_open = True
            CartUI()
    def adminportal(self):
        AdminPortal()
    def register(self):
        Register()
    def mycourse(self):
        self._window.destroy()
        MyCourse(self._username, self._user_type)
    def editprofile(self):
        pass
class LoginUI:
    def __init__(self):
        self.__font = 'Arial'
        self.__normal_size = 18
        self.__window = Tk()
        self.__window.title("CE MOOC")
        self.__window.geometry('300x300+0+0')
        self.__window.config(padx=20, pady=20)
        self.__window.resizable(width=False, height=False)
        self.__window.eval('tk::PlaceWindow . center')
        self._current_user = None
        self._current_user_type = None

        Label(self.__window, text="Login", font=(self.__font, self.__normal_size, 'bold')).grid(row=0, column=1)

        Label(self.__window, text="Username: ", font=(self.__font, self.__normal_size)).grid(row=1, column=1)
        self._username = StringVar()
        Entry(self.__window, textvariable=self._username).grid(row=1, column=2)
        Label(self.__window, text="Password: ", font=(self.__font, self.__normal_size)).grid(row=2, column=1)
        self._password = StringVar()
        Entry(self.__window, textvariable=self._password, show="*").grid(row=2, column=2)

        Button(self.__window, text="Guest", font=(self.__font, self.__normal_size),
               command=self.guest_button).grid(row=3, column=1)
        Button(self.__window, text="Login", fg='white', bg='green', font=(self.__font, self.__normal_size),
               command=self.lg).grid(row=3, column=2)

        self.__window.mainloop()

    def get_user_type(self,current_user):
        usdb = UserDataBase()
        user_db = usdb.get_user_db()
        username_list = []
        for i in range(len(user_db)):
            username_list.append(user_db[i][0])
        return user_db[username_list.index(current_user)][4]

    def lg(self):
        login = Login(self._username.get(), self._password.get())
        if not login.login():
            tkinter.messagebox.showerror(title="ERROR", message="User or Password not Match!")
        else:
            tkinter.messagebox.showinfo(title="Success", message="Login Complete!")
            self._current_user = self._username.get()
            self._current_user_type = self.get_user_type(self._current_user)
            self.__window.destroy()
            CourseUI(self._current_user, self._current_user_type)
    def guest_button(self):
        self.__window.destroy()
        CourseUI("Guest", "Guest")

class CartUI:
    def __init__(self):
        self.__font = 'Arial'
        self.__normal_size = 16
        self._window = Tk()
        self._window.title("CE MOOC")
        self._window.geometry('500x500+0+0')
        self._window.config(padx=20, pady=20)
        self._window.resizable(width=False, height=False)

        Label(self._window, text="Cart", font=(self.__font, self.__normal_size, 'bold')).grid(row=0, column=1)

        self._window.mainloop()

class AdminPortal:
    def __init__(self):
        self.__font = 'Arial'
        self.__normal_size = 16
        self._window = Tk()
        self._window.title("CE MOOC")
        self._window.geometry('500x500+0+0')
        self._window.config(padx=20, pady=20)
        self._window.resizable(width=False, height=False)

        Label(self._window, text="Admin Portal", font=(self.__font, self.__normal_size, 'bold')).grid(row=0, column=1)
        Button(self._window, text="User Management", font=(self.__font, self.__normal_size),
               command=self.crud_user).grid(row=1, column=0)

        self._window.mainloop()
    def crud_user(self):
        CrudUser()
class CrudUser:
    def __init__(self):
        self.__font = 'Arial'
        self.__normal_size = 16
        self._window = Toplevel()
        self._window.title("User Management")
        self._window.geometry('400x400+0+0')
        self._window.config(padx=20, pady=20)

        Label(self._window, text="Create User", font=(self.__font, self.__normal_size, 'bold')).grid(row=0, column=0)
        # --------------------------------- User Creation --------------------------------- #
        Label(self._window, text="Username: ", font=(self.__font, self.__normal_size)).grid(row=1, column=0)
        self._username = StringVar()
        self.__et1 = Entry(self._window, textvariable= self._username)
        self.__et1.grid(row=1, column=1)

        Label(self._window, text="Password: ", font=(self.__font, self.__normal_size)).grid(row=2, column=0)
        self._password = StringVar()
        self.__et2 = Entry(self._window, textvariable= self._password)
        self.__et2.grid(row=2, column=1)

        Label(self._window, text="First Name: ", font=(self.__font, self.__normal_size)).grid(row=3, column=0)
        self._fname = StringVar()
        self.__et3 = Entry(self._window, textvariable= self._fname)
        self.__et3.grid(row=3, column=1)

        Label(self._window, text="Last Name: ", font=(self.__font, self.__normal_size)).grid(row=4, column=0)
        self._lname = StringVar()
        self.__et4 = Entry(self._window, textvariable= self._lname)
        self.__et4.grid(row=4, column=1)

        Label(self._window, text="User Type: ", font=(self.__font, self.__normal_size)).grid(row=5, column=0)
        self._user_type = StringVar()
        self.__et5 = Entry(self._window, textvariable= self._user_type)
        self.__et5.grid(row=5, column=1)

        Button(self._window, text="Create", fg='white', bg='green', font=(self.__font, self.__normal_size),
               command=self.register).grid(row=5, column=2)

        # --------------------------------- User Deletion --------------------------------- #

        Label(self._window, text="Delete User", font=(self.__font, self.__normal_size, 'bold')).grid(row=6, column=0)
        Label(self._window, text="Username: ", font=(self.__font, self.__normal_size)).grid(row=7, column=0)
        self._user_deletion = StringVar()
        self.__et6 = Entry(self._window, textvariable=self._user_deletion)
        self.__et6.grid(row=7, column=1)
        Button(self._window, text="Delete", fg='white', bg='red', font=(self.__font, self.__normal_size),
               command=self.delete_user).grid(row=7, column=2)

        self._window.mainloop()

    def register(self):
        user = User()
        cuser = user.register(self._username.get(), self._password.get(),
                                self._fname.get(), self._lname.get(), self._user_type.get())
        print(cuser)
        if cuser == [] or self._username.get() == "" or self._password.get() == "" or self._fname.get() == "" or self._lname.get() == "" or self._user_type.get() == "":
            tkinter.messagebox.showerror(title="ERROR", message="Username Exists / Have blank Data")
        else:
            user_db = UserDataBase()
            user_db.add_user_to_db(cuser)
            print(user_db.get_user_db())
            self.clear_input()
            tkinter.messagebox.showinfo(title="Success", message="Registered!")

    def clear_input(self):
        self.__et1.delete(0, END)
        self.__et2.delete(0, END)
        self.__et3.delete(0, END)
        self.__et4.delete(0, END)
        self.__et5.delete(0, END)

    def delete_user(self):
        user = User()
        print(self._user_deletion.get())
        is_deleted = user.delete_user(self._user_deletion.get())
        if is_deleted:
            self.__et6.delete(0, END)
            tkinter.messagebox.showinfo(title="Success", message="Deletion success!")
        else:
            tkinter.messagebox.showerror(title="ERROR", message="Username not Found!")
class Register:
    def __init__(self):
        self.__font = 'Arial'
        self.__normal_size = 16
        self._window = Toplevel()
        self._window.title("User Management")
        self._window.geometry('400x400+0+0')
        self._window.config(padx=20, pady=20)

        Label(self._window, text="Register", font=(self.__font, self.__normal_size, 'bold')).grid(row=0, column=0)
        # --------------------------------- User Creation --------------------------------- #
        Label(self._window, text="Username: ", font=(self.__font, self.__normal_size)).grid(row=1, column=0)
        self._username = StringVar()
        self.__et1 = Entry(self._window, textvariable= self._username)
        self.__et1.grid(row=1, column=1)

        Label(self._window, text="Password: ", font=(self.__font, self.__normal_size)).grid(row=2, column=0)
        self._password = StringVar()
        self.__et2 = Entry(self._window, textvariable= self._password)
        self.__et2.grid(row=2, column=1)

        Label(self._window, text="First Name: ", font=(self.__font, self.__normal_size)).grid(row=3, column=0)
        self._fname = StringVar()
        self.__et3 = Entry(self._window, textvariable= self._fname)
        self.__et3.grid(row=3, column=1)

        Label(self._window, text="Last Name: ", font=(self.__font, self.__normal_size)).grid(row=4, column=0)
        self._lname = StringVar()
        self.__et4 = Entry(self._window, textvariable= self._lname)
        self.__et4.grid(row=4, column=1)


        Button(self._window, text="Create", fg='white', bg='green', font=(self.__font, self.__normal_size),
               command=self.register).grid(row=5, column=2)


        self._window.mainloop()
    def register(self):
        user = User()
        cuser = user.register(self._username.get(), self._password.get(),
                                self._fname.get(), self._lname.get(), "User")
        print(cuser)
        if cuser == [] or self._username.get() == "" or self._password.get() == "" or self._fname.get() == "" or self._lname.get() == "":
            tkinter.messagebox.showerror(title="ERROR", message="Username Exists / Have blank Data")
        else:
            user_db = UserDataBase()
            user_db.add_user_to_db(cuser)
            print(user_db.get_user_db())
            tkinter.messagebox.showinfo(title="Success", message="Registered!")
            self._window.destroy()

class MyCourse:
    def __init__(self, username, user_type):
        __user = User()
        __course_catalog = CourseCatalog()
        self._username = username
        self._user_type = user_type
        self.__font = 'Arial'
        self.__normal_size = 16
        self._window = Tk()
        self._window.title("My Course")
        self._window.geometry('600x600+0+0')
        self._window.config(padx=20, pady=20)

        menu = Menu()
        menu_item = Menu()
        menu_item.add_command(label='Edit Profile', command=self.edit_profile)
        menu_item.add_command(label='Browse Course', command=self.browse_course)
        menu_item.add_command(label='Logout', command=self.logout)
        self._window.config(menu=menu)
        menu.add_cascade(label="Your account: " + self._username, menu=menu_item)
        menu.add_cascade(label="About")
        Label(self._window, text="My Course", font=(self.__font, self.__normal_size)).grid(row=0, column=0)


        self._window.mainloop()
    def edit_profile(self):
        pass
    def browse_course(self):
        self._window.destroy()
        CourseUI(self._username, self._user_type)
    def logout(self):
        self._window.destroy()
        LoginUI()