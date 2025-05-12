import streamlit as st

#python -m venv venv
#.\venv\Scripts\Activate

def login():
    
    c1,c2,c3 = st.columns([1, 3, 1])
    with c1:
        st.empty()
    with c2:
        st.title("Neo Brain")
        #st.image("assets/bill.png")
        st.header("Inicio de sesión")
        if st.button("Log in"):
            st.login("auth0")
    with c3:
        st.empty()
    


def logout():
    st.title("Cerrar sesión")
    if st.button("Log out"):
        st.logout()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

chatbot = st.Page(
    "reports/chatbot.py", title="Chatbot", icon=":material/dashboard:", default=True
)
bugs = st.Page("reports/bugs.py", title="Bug report", icon=":material/bug_report:")
calendar = st.Page(
    "reports/calendar.py", title="Calendar", icon=":material/notification_important:"
)


search = st.Page("tools/search.py", title="Búsqueda", icon=":material/search:")
history = st.Page("tools/history.py", title="Historial", icon=":material/history:")

if st.experimental_user.is_logged_in:
    pg = st.navigation(
        {
            "Cuenta": [logout_page],
            "Herramientas": [chatbot, calendar, bugs],
            "Tools": [search, history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
