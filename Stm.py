# import streamlit as st

# # st.markdown("<h2 style='color:green;'>Students Registration App<h2>", unsafe_allow_html=True)


# # if "student" not in st.session_state:
# #     st.session_state["student"] = {}



# # st.header("Registration Form")
# # with st.form("User_Form"):
# #     name=st.text_input("Name")
# #     Age=st.number_input("Age",min_value=5,max_value=120)
# #     course=st.selectbox("Choose course",["ICT","Math","Science","Physics"])
# #     submit=st.form_submit_button("submit form")

# # if submit:
# #     st.session_state["student"]["Name"]=name
# #     st.session_state["student"]["Age"]=Age
# #     st.session_state['student']["Course"]=course
# #     st.success("Form submitted successfully")

# # # stored a dictionary using session state
# # if st.session_state["student"]:
# #     st.header("Details from last session")
# #     st.write("Name",st.session_state["student"]["Name"])
# #     st.write("Age",st.session_state["student"]["Age"])
# #     st.write("Course",st.session_state["student"]["Course"])




# # multiple users with list
# # import streamlit as st

# # st.markdown("<h2 style='color:pink;'>Welcome to multiple users detail storage app</h2>",unsafe_allow_html=True)
# # # initialize session state
# # if "student" not in st.session_state:
# #     st.session_state["student"]=[]

# # # form inputs
# # with st.form("User_form"):
# #     st.subheader("Fill all fields")
# #     name=st.text_input("Name")
# #     age=st.number_input("Age",min_value=1)
# #     address=st.text_input("Address")
# #     # submit button
# #     submit=st.form_submit_button("submit form")

# # # save in dic
# # if submit and name.strip():
# #     student={"name":name,
# #              "age":age,
# #              "address":address}
    
# #     st.session_state["student"].append(student)
# #     st.success("Form submitted successfully")



# # # check
# # if st.session_state['student']:
# #     st.subheader("Registered students")
# #     # display
# #     for i ,num in enumerate(st.session_state["student"],start=1):
# #         st.write(f"sudent {i}")
# #         st.write(f"Name", num["name"])
# #         st.write(f"Age", num["age"])
# #         st.write(f"Address", num["address"])
# #         st.markdown("-------------------")

# # st.markdown("--------------bamm--------------")




# # import streamlit as st
# # import pandas as pd

# # st.markdown("<h1 style='color:yellow;'> Student Registration System</h1>",unsafe_allow_html=True)





# # # initialize session state
# # if "student" not in st.session_state:
# #     st.session_state["student"]=[]

# # # clear form fields
# # # def reset_form():
# # #     st.session_state.name = ""
# # #     st.session_state.age = 1
# # #     st.session_state.address = ""



# # # form inputs
# # with st.form("User_form"):
# #     st.subheader("Fill all fields")
# #     name=st.text_input("Name",key="name")
# #     age=st.number_input("Age",min_value=1,key="age")
# #     address=st.text_input("Address",key="address")
# #     # submit button
# #     submit = st.form_submit_button(
# #         "Submit",
# #     )




# # # save in dic
# # if submit:
# #     student={"name":st.session_state.name,
# #              "age":st.session_state.age,
# #              "address":st.session_state.address}
# #     st.session_state["student"].append(student)
# #     st.success("Form submitted successfully")


# # # check
# # if st.session_state['student']:
# #     # convert list to dataframe
# #     df=pd.DataFrame(st.session_state["student"])
# #     st.markdown("<h2 style='color:yellow;'>Registered students(Table view)</h2>",unsafe_allow_html=True)
# #     st.dataframe(df)

# #     st.write("Total students",len(df))

# #     if st.button("Clear available students"):
# #         st.session_state["student"]=[]
# #         st.success("All registered students deleted successfully")
# #         st.rerun()
    




# # st.markdown(
# #     "<h3 style='color:lightgray;'>"
# #     "<b>About this App</b><br>"
# #     "A simple student registration and records dashboard built with "
# #     "<b>Python</b> and <b>Streamlit</b>. "
# #     "It demonstrates form handling, session state management, "
# #     "and dynamic data presentation for learning and revision purposes."
# #     "</h3>",
# #     unsafe_allow_html=True
# # )

# # import streamlit as st
# # import pandas as pd
# # # title
# # st.markdown("<h1 style='color:yellow'> 🎓 Administrative / Management Dashboard</h1>",unsafe_allow_html=True)

# # # function to clear details
# # def clear():
# #     st.session_state["student"]=[]
# #     st.success("Data clear successfully")
# #     st.rerun()
    

# # # Initialize session state
# # if "student" not in st.session_state:
# #     st.session_state["student"] = []

# # if "counter" not in st.session_state:
# #     st.session_state.counter = 1


# # st.sidebar.markdown("<h3 style='color:yellow'> Student System </h3>", unsafe_allow_html=True)
# # page = st.sidebar.radio(
# #     "Navigation",
# #     ["Home", "Register", "Manage Records", "About"]
# # )


# # if page == "Home":
# #     st.title("🎓 Student Registration System")

# #     total = len(st.session_state["student"])
# #     st.metric("Total Students", total)

# #     st.write("Welcome! Use the sidebar to register and manage students.")



# # elif page == "Register":
# #     st.title("📝 Register Student")

# #     with st.form("register_form", clear_on_submit=True):
# #         name = st.text_input("Student Name")
# #         age = st.number_input("Age", min_value=1, step=1)
# #         course = st.text_input("Course")

# #         submitted = st.form_submit_button("Register")

# #     if submitted and name.strip():
# #         student_id = st.session_state.counter
# #         st.session_state.counter += 1

# #         st.session_state["student"].append({
# #             "id": student_id,
# #             "name": name,
# #             "age": age,
# #             "course": course
# #         })

# #         st.success("Student registered successfully")

# # elif page == "Manage Records":
  
# #     if st.session_state["student"]:
# #         df = pd.DataFrame(st.session_state["student"])
# #         st.dataframe(df, use_container_width=True)

# #         # -------- DELETE SECTION --------
# #         st.markdown("<h3 style='color:yellow'> Delete Student </h3>", unsafe_allow_html=True)

    
# #         delete_id = st.selectbox(
# #             "Select student to delete",
# #             df["id"].tolist(),
# #             key="delete_select"
# #         )

# #         if st.button("Delete student", key="delete_btn"):
# #             st.session_state["student"] = [
# #                 s for s in st.session_state["student"] if s["id"] != delete_id
# #             ]
# #             st.success("Student deleted successfully")
# #             st.rerun()

# #         if st.button("Clear all data", key="clear_btn"):
# #             clear()

# #         # -------- EDIT SECTION --------
# #         st.markdown("<h3 style='color:yellow'> Edit Student </h3>", unsafe_allow_html=True)

# #         edit_id = st.selectbox(
# #             "Select student to edit",
# #             df["id"].tolist(),
# #             key="edit_select"
# #         )

# #         selected_student = next(
# #             (s for s in st.session_state["student"] if s["id"] == edit_id),
# #             None
# #         )

# #         if selected_student:
# #             with st.form("Edit_Form"):
# #                 name = st.text_input("Name", value=selected_student["name"])
# #                 age = st.number_input("Age", min_value=1, value=selected_student["age"])
# #                 course = st.text_input("Course", value=selected_student["course"])
# #                 update = st.form_submit_button("Update student")

# #             if update:
# #                 for s in st.session_state["student"]:
# #                     if s["id"] == selected_student["id"]:
# #                         s["name"] = name
# #                         s["age"] = age
# #                         s["course"] = course
# #                         break

# #                 st.success("Student updated successfully")
# #                 st.rerun()



# # # about section
# # elif page == "About":
# #     st.title("ℹ️ About")

# #     st.write("""
# #     This Student Registration System was built using **Streamlit**.

# #     **Features:**
# #     - Register students
# #     - View records
# #     - Delete records
# #     - Persistent session state

# #     **Built for learning and real-world practice.**
# #     """)

# # st.sidebar.markdown("---")
# # st.sidebar.caption("Version 1.0 • Student Management Dashboard")

















# # import streamlit  as st
# # import pandas as pd
# # # title
# # st.markdown("<h2 style='color:skyblue;'>Welcome to Impact Nexus.net</h2>",unsafe_allow_html=True)


# # st.sidebar.markdown("<h4 style='color:skyblue;'>Student Management System</h4>",unsafe_allow_html=True)
# # page=st.sidebar.radio("Select Page",["Home","Register","Manage","About"])

# # if page=="Home":
# #     st.markdown("<h5 style='color:Green;'>Consistent is Attractive</h5>",unsafe_allow_html=True)
# #     Total=len(st.session_state["student"])
# #     st.metric("Total number of sudents",Total)
# #     st.write("Welcome! Use the Navigation bar to move throught the app")


# # if page=="Register":
# #     # initialize session state
# #     if "student" not in st.session_state:
# #         st.session_state["student"]=[]

# #     # create form
# #     st.subheader("User Form")
# #     with st.form("User_form",clear_on_submit=True):
# #         name=st.text_input("Name")
# #         age=st.number_input("Age",min_value=1)
# #         gender=st.text_input("Gender")
# #         course=st.text_input("Course")
# #         submit=st.form_submit_button("submit")

# #     # save detail in a dict
# #     if submit and name.strip():
# #         students={"name":name,
# #                 "age":age,
# #                 "gender":gender,
# #                 "course":course
# #                 }
# #         st.session_state["student"].append(students)
# #         st.success("Form submitted successfully!")
    
# # if page=="Manage":
# # # save detail in a session sate list
# #     if st.session_state["student"]:

# #         # display details using table
# #         st.subheader("Registered students")
# #         df=pd.DataFrame(st.session_state["student"])
# #         st.table(df)
# #         st.subheader(f"Available students: {len(st.session_state["student"])}")


# # # about section
# # elif page == "About":
# #     st.title("ℹ️ About")

# #     st.write("""
# #     This Student Registration System was built using **Streamlit**.

# #     **Features:**
# #     - Register students
# #     - View records
# #     - Delete records
# #     - Persistent session state

# #     **Built for learning and real-world practice.**
# #     """)





# #     st.markdown(
# #     "<h3 style='color:orange; border-bottom:2px solid #ccc;'>Developed By Iddrisu Inusah Adelga (Impact)</h3>",
# #     unsafe_allow_html=True
# #     )



# # st.sidebar.markdown("---")
# # st.sidebar.caption("Version 1.0 • Student Management Dashboard")

# import streamlit as st
# import pandas as pd

# st.title("Welcome Once Again!")

# # innitialize session state
# if "student" not in st.session_state:
#     st.session_state["student"]=[]

# # innitialize counter
# if "count" not in st.session_state:
#     st.session_state.count=1

# # clear function
# def clear():
#     st.session_state["student"]=[]
#     st.rerun()
#     st.success("success")   


# # create the form
# st.subheader("Registration Form")

# with st.form("User_form",clear_on_submit=True):
#     name=st.text_input("Name")
#     age=st.number_input("Age",min_value=1)
#     course=st.text_input("Course")
#     submit=st.form_submit_button("submit form")

# if submit and name.strip():
#     st.success("success")
#     student_id=st.session_state.count
#     st.session_state.count +=1

#     students={
#            "student_id":student_id,
#           "name":name,
#           "age":age,
#           "course":course}
#     st.session_state["student"].append(students)

# if st.session_state["student"]:
#     df=pd.DataFrame(st.session_state["student"])
#     st.dataframe(df,use_container_width=True)

# # delete section
#     delete_id=st.selectbox("Select to delete", df["student_id"].tolist(),key="id_delet")


#     if st.button("Delete student",key="delete_btn"):
#         st.session_state["student"]=[s for s in st.session_state["student"] if s["student_id"] != delete_id]

#         st.rerun()
#         st.success("success")
    
#     if st.button("clear form", key="clear"):
#         clear()
        
#         st.rerun()
#         st.success("success")
#     # edit section

# #    create selectbox
#     id_edit=st.selectbox("select to edit",df["student_id"],key="edit_")

#     # create a comparison variable
#     selected_student=next(s for s in st.session_state["student"] if s["student_id"]==id_edit)

#     if selected_student:
#         with st.form("edit_form"):
#             name=st.text_input("Name",value=selected_student["name"])
#             age=st.number_input("Age",value=selected_student["age"])
#             course=st.text_input("Course",selected_student['course'])
#             update=st.form_submit_button("Update student")

#     if update:
#         for s in st.session_state["student"]:
#             if s["student_id"]==selected_student["student_id"]:
#                 s["name"]=name
#                 s["age"]=age
#                 s["course"]=course
#                 break
#         st.success("success")
#         st.rerun()
#     # id_edit=st.selectbox("select to edit",df["student_id"],key="edit_")

#     # selected_student=next(s for s in st.session_state['student'] if s["student_id"]==id_edit)
#     # if selected_student:
#     #     with st.form("edit_form"):
#     #         name=st.text_input("name",value=selected_student["name"])
#     #         age=st.number_input("Age",value=selected_student["age"])
#     #         course=st.text_input("Course",value=selected_student["course"])
#     #         update=st.form_submit_button("Update student")

#     # if update:
#     #     for s in st.session_state["student"]:
#     #         if s["student_id"]==selected_student["student_id"]:
#     #             s["name"]=name
#     #             s["age"]=age
#     #             s["course"]=course
#     #             break
#     #     st.success("success")
#     #     st.rerun()




# import streamlit as st
# import pandas as pd





# def init_state():
#     if "student" not in st.session_state:
#         st.session_state["student"] = []

#     if "counter" not in st.session_state:
#         st.session_state.counter = 1

# def register_student():
#     st.subheader("Registration form")

#     with st.form("User_form", clear_on_submit=True):
#         name = st.text_input("Name")
#         age = st.number_input("Age", min_value=1)
#         course = st.text_input("Course")
#         submit = st.form_submit_button("Submit form")

#     if submit and name.strip() and course.strip():
#         student_id = st.session_state.counter
#         st.session_state.counter += 1

#         student = {
#             "student_id": student_id,
#             "name": name,
#             "age": age,
#             "course": course
#         }

#         st.session_state["student"].append(student)
#         st.success("Student registered successfully")


# def show_students():
#     if not st.session_state["student"]:
#         st.info("No students registered yet.")
#         return None

#     df = pd.DataFrame(st.session_state["student"])
#     st.dataframe(df, use_container_width=True)
#     return df


# def delete_student(df):
#     delete_id = st.selectbox(
#         "Select student to delete",
#         df["student_id"].tolist(),
#         key="delete_select"
#     )

#     if st.button("Delete student"):
#         st.session_state["student"] = [
#             s for s in st.session_state["student"]
#             if s["student_id"] != delete_id
#         ]
#         st.rerun()



# def clear_students():
#     if st.button("Clear students"):
#         st.session_state["student"] = []
#         st.rerun()




# def edit_student(df):
#     edit_id = st.selectbox(
#         "Select student to edit",
#         df["student_id"].tolist(),
#         key="edit_select"
#     )

#     selected_student = next(
#         (s for s in st.session_state["student"] if s["student_id"] == edit_id),
#         None
#     )

#     if not selected_student:
#         return

#     with st.form("edit_form"):
#         name = st.text_input("Name", value=selected_student["name"])
#         age = st.number_input("Age", value=selected_student["age"])
#         course = st.text_input("Course", value=selected_student["course"])
#         update = st.form_submit_button("Update student")

#     if update:
#         for s in st.session_state["student"]:
#             if s["student_id"] == selected_student["student_id"]:
#                 s["name"] = name
#                 s["age"] = age
#                 s["course"] = course
#                 break

#         st.success("Student updated successfully")
#         st.rerun()





# st.title("Refactor")

# init_state()
# register_student()

# df = show_students()

# if df is not None:
#     delete_student(df)
#     clear_students()
#     edit_student(df)




import streamlit as st
import pandas as pd

import os


st.set_page_config(page_title="Student Manager", layout="wide")

DATA_FILE = "students.csv"

def load_students():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE).to_dict("records")
    return []




def save_students():
    pd.DataFrame(st.session_state["student"]).to_csv(DATA_FILE, index=False)


# innitializarions
def init_state():
    if "student" not in st.session_state:
        st.session_state["student"] = load_students()
        save_students()

    if "counter" not in st.session_state:
        st.session_state.counter = 1

# register form
def register_student():
    st.markdown("## 📝 Student Registration")

    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)
        course = st.text_input("Course")
        submit = st.form_submit_button("Register")

    if submit and name.strip() and course.strip():
        student = {
            "student_id": st.session_state.counter,
            "name": name,
            "age": age,
            "course": course
        }
        st.session_state.counter += 1
        st.session_state["student"].append(student)
        save_students()
        st.success("Student registered successfully 🎉")






def show_students():
    if not st.session_state["student"]:
        st.info("No students registered yet.")
        return None

    df = pd.DataFrame(st.session_state["student"])
    st.dataframe(df, use_container_width=True)
    return df



# delete logic
def delete_student(df):
    
    st.markdown(
    "<h3 style='color:orange; border-bottom:2px solid #ccc;'>🗑 Delete Student</h3>",
    unsafe_allow_html=True
    )

    delete_id = st.selectbox(
        "Select student ID",
        df["student_id"].tolist(),key="delet_"
    )

    if st.button("Delete student"):
        st.session_state["student"] = [
            s for s in st.session_state["student"]
            if s["student_id"] != delete_id
        ]
        save_students()
        st.success("Student deleted")
        st.rerun()



# edit logic
def edit_student(df):
    st.markdown(
    "<h3 style='color:green; border-bottom:2px solid #ccc;'> ✏ Edit Student</h3>",
    unsafe_allow_html=True
    )
    
    edit_id = st.selectbox(
        "Select student ID",
        df["student_id"].tolist(),key="edit_"
    )

    selected_student = next(
        (s for s in st.session_state["student"] if s["student_id"] == edit_id),
        None
    )

    if not selected_student:
        return

    with st.form("edit_form"):
        name = st.text_input("Name", value=selected_student["name"])
        age = st.number_input("Age", value=selected_student["age"])
        course = st.text_input("Course", value=selected_student["course"])
        update = st.form_submit_button("Update")

    if update:
        for s in st.session_state["student"]:
            if s["student_id"] == edit_id:
                s.update({"name": name, "age": age, "course": course})
                save_students()
                break
        st.success("Student updated successfully")
        st.rerun()

# home page
def home_page():
    st.markdown(
        """
        # 🎓 Student Management System  
        *Simple. Clean. Educational.*
        """
    )

    total_students = len(st.session_state["student"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Registered Students", total_students)
    col2.metric("System Status", "Active")
    col3.metric("App Version", "1.0")

    st.markdown("---")

    st.markdown(
        """
        ### 👋 Welcome  
        This system helps you **register**, **edit**, and **manage** student records
        efficiently using modern Python tools.
        """
    )

# manage page
def manage_page():
    st.markdown("<h3 style='color:gold'>  Manage Students</h3>", unsafe_allow_html=True)

    df = show_students()
    if df is not None:
        col1, col2 = st.columns(2)
        with col1:
            delete_student(df)
        with col2:
            edit_student(df)


# about page
def about_page():
    st.markdown(
        """
        ## ℹ️ About This App

        This Student Management App was built using **Streamlit** and **Python**.

        ### 🚀 Features
        - Register students
        - Edit student records
        - Delete students
        - Dashboard statistics

        ### 👨‍💻 Built for learning & growth
        Designed to help learners understand **state management**, **CRUD logic**, 
        and **UI structuring** in Python.
        """
    )
    st.markdown(
    "<h3 style='color:orange; border-bottom:2px solid #ccc;'>Developed By Iddrisu Inusah Adelga (Impact)</h3>",
    unsafe_allow_html=True
    )



# main app logic
def main():
    init_state()

    st.sidebar.markdown(
    "<h3 style='color:orange; border-bottom:2px solid #ccc;'> Navigation</h3>",
    unsafe_allow_html=True
    )
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Register", "Manage", "About"]
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Version 1.0 • Student Management Dashboard")

    if page == "Home":
        home_page()
    elif page == "Register":
        register_student()
    elif page == "Manage":
        manage_page()
    elif page == "About":
        about_page()

# run main app
main()












