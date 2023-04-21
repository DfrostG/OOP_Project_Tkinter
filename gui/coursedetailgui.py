import tkinter
from tkinter import messagebox
import customtkinter
import requests
import json

from gui.cartgui import CartGUI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class CourseDetail:
    def __init__(self, username, refcode, user_type):
        self.__refcode = refcode
        self.__username = username
        self.__user_type = user_type
        self.__cdata = self.get_course()
        self.__labels = {
            'Refcode': self.__cdata['_Courses__refcode'],
            'Title': self.__cdata['_Courses__title'],
            'Description': self.__cdata['_Courses__desc'],
            'Teacher': self.__cdata['_Courses__teacher'],
            'Category': self.__cdata['_Courses__catg'],
            'Target Audience': self.__cdata['_Courses__target'],
            'Objective': self.__cdata['_Courses__objective'],
            'Total Hours': self.__cdata['_Courses__hour'],
            'Recommended Hours': self.__cdata['_Courses__recom_hour'],
            'Release Date': self.__cdata['_Courses__release'],
            'Contact Email': self.__cdata['_Courses__contact']
        }
        # --- Create GUI --- #
        self.__cdetail = customtkinter.CTkToplevel()
        self.__cdetail.geometry("500x500")
        self.__cdetail.resizable(width=False, height=False)
        self.__cdetail.title(refcode)
        self.__header_font = customtkinter.CTkFont(family="Kanit", weight="bold", size=20)
        self.__normal_font = customtkinter.CTkFont(family="Kanit", weight="normal", size=16)
        self.__txtbox_font = customtkinter.CTkFont(family="Kanit", weight="normal", size=12)
        customtkinter.CTkLabel(self.__cdetail, text=self.__refcode, font=self.__header_font).pack()
        customtkinter.CTkLabel(self.__cdetail, text=self.__cdata['_Courses__title'], font=self.__header_font).pack()
        if self.__user_type not in ["Guest", "Admin"]:
            if not self.check_enrolled():
                customtkinter.CTkButton(self.__cdetail, text="Enroll", font=self.__normal_font, command=self.add_cart).pack()
            else:
                customtkinter.CTkLabel(self.__cdetail, text="You have enrolled!", font=self.__normal_font, text_color="red").pack()
        else:
            customtkinter.CTkLabel(self.__cdetail, text="You cannot enrolled!", font=self.__normal_font, text_color="red").pack()
        for i, (key, value) in enumerate(self.__labels.items()):
            customtkinter.CTkLabel(self.__cdetail, text=key + ":", font=self.__normal_font).place(x=25, y=125 + (25 * i))
            customtkinter.CTkLabel(self.__cdetail, text=value, font=self.__normal_font).place(x=200, y=125 + (25 * i))
        self.__cdetail.mainloop()

    def get_course(self):
        url = "http://localhost:8000/courses/"+self.__refcode
        r = requests.get(url)
        data = json.loads(r.text)
        print(data)
        return data
    def check_enrolled(self):
        url = "http://localhost:8000/enrolled?username="+self.__username
        r = requests.get(url)
        data = json.loads(r.text)
        for i in data:
            if i["_Courses__refcode"] == self.__refcode:
                return True
            else:
                return False
    def add_cart(self):
        add_cart = {
            "username": self.__username,
            "refcode": self.__refcode
        }
        r = requests.post("http://localhost:8000/addcart", json=add_cart)
        res = json.loads(r.text)
        print(res)
        if res == {"Cart": "Success"}:
            tkinter.messagebox.showinfo(title="Success", message="Added to Cart!")
            self.__cdetail.destroy()
            CartGUI(self.__username)

#CourseDetail("ffwatcharin","HARD001","Student")