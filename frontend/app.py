import streamlit as st

from services.api import login, get_dashboard

st.set_page_config(
    page_title="SkyLog",
    page_icon="✈️",
    layout="centered"
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


if not st.session_state["logged_in"]:

    st.title("✈️ SkyLog")

    st.subheader("Electronic Flight Logbook")

    st.divider()

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = login(
            email,
            password
        )

        if response.status_code == 200:

            st.session_state["token"] = (
                response.json()["access_token"]
            )

            st.session_state["logged_in"] = True

            st.rerun()

        else:

            st.error("Invalid email or password.")



else:

    st.sidebar.title("✈️ SkyLog")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Aircraft",
            "Flights",
            "Reports"
        ]
    )

    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.rerun()

    if page == "Dashboard":

        dashboard = get_dashboard(
            st.session_state["token"]
        )

        if dashboard.status_code != 200:

            st.error("Unable to load dashboard.")

            st.stop()

        data = dashboard.json()

        st.title("Dashboard")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "✈ Flights",
                data["total_flights"]
            )

            st.metric(
                "🛬 Landings",
                data["total_landings"]
            )

        with col2:

            st.metric(
                "⏱ Hours",
                data["total_hours"]
            )

            st.metric(
                "🛩 Aircraft",
                data["aircraft_owned"]
            )

    elif page == "Aircraft":

        st.title("Aircraft")

        st.info("Aircraft module coming next.")

    elif page == "Flights":

        st.title("Flights")

        st.info("Flights module coming next.")

    elif page == "Reports":

        st.title("Reports")

        st.info("Reports module coming next.")