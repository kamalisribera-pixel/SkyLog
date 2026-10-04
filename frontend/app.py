import streamlit as st

from services.api import (
    login,
    register,
    get_dashboard,
    get_aircraft,
    create_aircraft,
    update_aircraft,
    delete_aircraft,
    get_flights,
    create_flight,
    delete_flight,
    export_csv,
    get_statistics,
)

st.set_page_config(page_title="SkyLog", page_icon="✈️", layout="centered")


def load_css():

    with open("assets/style.css") as f:

        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


if "logged_in" not in st.session_state:

    st.session_state["logged_in"] = False


# =========================
# LOGIN PAGE CLEANUP
# =========================
if not st.session_state["logged_in"]:

    # Hide sidebar and menu on authentication page
    st.markdown(
        """
        <style>

        [data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="collapsedControl"] {
            display: none !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    if "auth_page" not in st.session_state:

        st.session_state["auth_page"] = "Login"

    st.title("✈️ SkyLog")

    st.caption("Electronic Flight Logbook")

    st.divider()

    # ==========================
    # AUTH SWITCH
    # ==========================

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Login", use_container_width=True):

            st.session_state["auth_page"] = "Login"

            st.rerun()

    with col2:

        if st.button("Register", use_container_width=True):

            st.session_state["auth_page"] = "Register"

            st.rerun()

    st.divider()

    # ==========================
    # LOGIN
    # ==========================

    if st.session_state["auth_page"] == "Login":

        st.subheader("Welcome Back")

        email = st.text_input("Email", key="login_email")

        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Sign In", use_container_width=True):

            response = login(email, password)

            if response.status_code == 200:

                st.session_state["token"] = response.json()["access_token"]

                st.session_state["logged_in"] = True

                st.rerun()

            else:

                st.error("Invalid email or password.")

    # ==========================
    # REGISTER
    # ==========================

    else:

        st.subheader("Create Account")

        name = st.text_input("Name", key="register_name")

        email = st.text_input("Email", key="register_email")

        password = st.text_input("Password", type="password", key="register_password")

        if st.button("Create Account", use_container_width=True):

            response = register(name, email, password)

            if response.status_code in [200, 201]:

                st.success("Account created successfully. Please login.")

                st.session_state["auth_page"] = "Login"

            else:

                st.error(response.text)

else:

    st.sidebar.title("✈️ SkyLog")

    st.sidebar.caption("Electronic Flight Logbook")

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation", ["Dashboard", "Aircraft", "Flights", "Reports"]
    )
    st.sidebar.divider()

    st.sidebar.write("🧑 Pilot Session Active")

    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.rerun()
    if page == "Dashboard":

        dashboard = get_dashboard(st.session_state["token"])

        if dashboard.status_code != 200:

            st.error("Unable to load dashboard.")
            st.stop()

        data = dashboard.json()

        st.title("✈️ Flight Dashboard")

        st.caption("Overview of your flight activity")

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(label="✈ Flights", value=data["total_flights"])

        with col2:

            st.metric(label="⏱ Flight Hours", value=f"{data['total_hours']} hrs")

        with col3:

            st.metric(label="🛬 Landings", value=data["total_landings"])

        with col4:

            st.metric(label="🛩 Aircraft", value=data["aircraft_owned"])

        st.divider()

        st.subheader("Recent Activity")

        st.info("Recent flight history will appear here.")

    elif page == "Aircraft":

        st.title("✈ Aircraft")

        # =========================
        # ADD AIRCRAFT
        # =========================

        st.subheader("Add Aircraft")

        registration = st.text_input("Registration")

        manufacturer = st.text_input("Manufacturer")

        model = st.text_input("Model")

        aircraft_type = st.selectbox(
            "Aircraft Type", ["Single Engine", "Multi Engine", "Helicopter", "Jet"]
        )

        engine_type = st.selectbox("Engine Type", ["Piston", "Turboprop", "Jet"])

        if st.button("Add Aircraft"):

            response = create_aircraft(
                st.session_state["token"],
                {
                    "registration": registration,
                    "manufacturer": manufacturer,
                    "model": model,
                    "aircraft_type": aircraft_type,
                    "engine_type": engine_type,
                },
            )

            if response.status_code == 201:

                st.success("Aircraft added successfully!")

                st.rerun()

            else:

                st.error(response.text)

        st.divider()

        # =========================
        # AIRCRAFT LIST
        # =========================

        st.subheader("My Aircraft")

        response = get_aircraft(st.session_state["token"])

        if response.status_code != 200:

            st.error("Unable to load aircraft.")

        else:

            aircraft_list = response.json()

            if len(aircraft_list) == 0:

                st.info("No aircraft added.")

            else:

                for aircraft in aircraft_list:

                    with st.container():

                        col1, col2, col3 = st.columns([4, 1, 1])

                        with col1:

                            st.markdown(
                                f"""
                            <div class="aircraft-card">

                            <h3>🛩 {aircraft['registration']}</h3>

                            <p>
                            <b>Manufacturer:</b> {aircraft['manufacturer']}<br>

                            <b>Model:</b> {aircraft['model']}<br>

                            <b>Type:</b> {aircraft['aircraft_type']}<br>

                            <b>Engine:</b> {aircraft['engine_type']}
                            </p>

                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                        with col2:

                            if st.button("✏️", key=f"edit_{aircraft['aircraft_id']}"):

                                st.session_state["edit_aircraft"] = aircraft

                                st.session_state["edit_mode"] = True

                                st.rerun()

                        with col3:

                            if st.button("🗑", key=f"delete_{aircraft['aircraft_id']}"):

                                delete_aircraft(
                                    st.session_state["token"], aircraft["aircraft_id"]
                                )

                                st.rerun()

        # =========================
        # EDIT AIRCRAFT
        # =========================

        if st.session_state.get("edit_mode", False):

            st.divider()

            st.subheader("Edit Aircraft")

            aircraft = st.session_state["edit_aircraft"]

            edit_registration = st.text_input(
                "Registration", value=aircraft["registration"]
            )

            edit_manufacturer = st.text_input(
                "Manufacturer", value=aircraft["manufacturer"]
            )

            edit_model = st.text_input("Model", value=aircraft["model"])

            edit_type = st.selectbox(
                "Aircraft Type",
                ["Single Engine", "Multi Engine", "Helicopter", "Jet"],
                index=["Single Engine", "Multi Engine", "Helicopter", "Jet"].index(
                    aircraft["aircraft_type"]
                ),
            )

            edit_engine = st.selectbox(
                "Engine Type",
                ["Piston", "Turboprop", "Jet"],
                index=["Piston", "Turboprop", "Jet"].index(aircraft["engine_type"]),
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("Save Changes"):

                    response = update_aircraft(
                        st.session_state["token"],
                        aircraft["aircraft_id"],
                        {
                            "registration": edit_registration,
                            "manufacturer": edit_manufacturer,
                            "model": edit_model,
                            "aircraft_type": edit_type,
                            "engine_type": edit_engine,
                        },
                    )

                    if response.status_code == 200:

                        st.success("Aircraft updated successfully!")

                        st.session_state["edit_mode"] = False

                        st.rerun()

                    else:

                        st.error(response.text)

            with col2:

                if st.button("Cancel"):

                    st.session_state["edit_mode"] = False

                    st.rerun()

    elif page == "Flights":

        st.title("✈ Flights")

        st.caption("Record and manage your flight logbook")

        st.divider()

        # =========================
        # LOAD AIRCRAFT
        # =========================

        aircraft_response = get_aircraft(st.session_state["token"])

        if aircraft_response.status_code != 200:

            st.error("Unable to load aircraft.")

            st.stop()

        aircraft_list = aircraft_response.json()

        if len(aircraft_list) == 0:

            st.warning("Please add an aircraft before logging a flight.")

            st.stop()

        # =========================
        # ADD FLIGHT
        # =========================

        st.subheader("Log New Flight")

        aircraft_options = {
            f"{a['registration']} - {a['manufacturer']} {a['model']}": a["aircraft_id"]
            for a in aircraft_list
        }

        selected_aircraft = st.selectbox("Aircraft", list(aircraft_options.keys()))

        flight_date = st.date_input("Flight Date")

        col1, col2 = st.columns(2)

        with col1:

            departure_airport = st.text_input("Departure Airport")

        with col2:

            arrival_airport = st.text_input("Arrival Airport")

        col1, col2 = st.columns(2)

        with col1:

            flight_time = st.number_input(
                "Flight Time (Hours)", min_value=0.1, step=0.1
            )

        with col2:

            landings = st.number_input("Landings", min_value=1, step=1)

        day_night = st.selectbox("Day / Night", ["Day", "Night"])

        remarks = st.text_area("Remarks")

        if st.button("Save Flight"):

            response = create_flight(
                st.session_state["token"],
                {
                    "aircraft_id": aircraft_options[selected_aircraft],
                    "flight_date": str(flight_date),
                    "departure_airport": departure_airport,
                    "arrival_airport": arrival_airport,
                    "flight_time": flight_time,
                    "landings": landings,
                    "day_night": day_night,
                    "remarks": remarks,
                },
            )

            if response.status_code == 201:

                st.success("Flight logged successfully!")

                st.rerun()

            else:

                st.error(response.text)

        st.divider()

        # =========================
        # RECENT FLIGHTS
        # =========================

        st.subheader("Recent Flights")

        response = get_flights(st.session_state["token"])

        if response.status_code != 200:

            st.error("Unable to load flights.")

        else:

            data = response.json()

            flights = data["flights"]

            if len(flights) == 0:

                st.info("No flights logged.")

            else:

                for flight in flights:

                    aircraft_name = next(
                        (
                            a["registration"]
                            for a in aircraft_list
                            if a["aircraft_id"] == flight["aircraft_id"]
                        ),
                        "Unknown",
                    )

                    with st.container():

                        st.markdown(
                            f"""
                        <div class="flight-card">

                        <h3>✈ {flight['flight_date']}</h3>

                        <b>Aircraft:</b> {aircraft_name}<br>

                        <b>Route:</b>
                        {flight['departure_airport']} ➜ {flight['arrival_airport']}

                        <br><br>

                        <b>Time:</b> {flight['flight_time']} hrs

                        <br>

                        <b>Landings:</b> {flight['landings']}

                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                        if st.button(
                            "🗑 Delete", key=f"delete_flight_{flight['flight_id']}"
                        ):

                            delete_response = delete_flight(
                                st.session_state["token"], flight["flight_id"]
                            )

                            if delete_response.status_code == 200:

                                st.success("Flight deleted successfully!")

                                st.rerun()

                            else:

                                st.error(delete_response.text)

                        st.divider()

    elif page == "Reports":

        st.title("📊 Flight Reports")

        st.caption("Flight statistics and logbook export")

        st.divider()

        # =========================
        # STATISTICS
        # =========================

        statistics = get_statistics(st.session_state["token"])

        if statistics.status_code != 200:

            st.error("Unable to load statistics.")

            st.stop()

        data = statistics.json()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric("✈ Total Flights", data["total_flights"])

        with col2:

            st.metric("⏱ Total Hours", f"{data['total_hours']} hrs")

        with col3:

            st.metric("🛬 Total Landings", data["total_landings"])

        with col4:

            st.metric("📈 Average Flight", f"{data['average_flight_time']} hrs")

        st.divider()

        # =========================
        # PERFORMANCE
        # =========================

        st.subheader("Flight Performance")

        col1, col2 = st.columns(2)

        with col1:

            st.info(f"""
    **Longest Flight**

    {data['longest_flight']} hours
    """)

        with col2:

            st.info(f"""
    **Average Flight**

    {data['average_flight_time']} hours
    """)

        st.divider()

        # =========================
        # EXPORT
        # =========================

        st.subheader("Export Flight Log")

        if st.button("Generate CSV"):

            response = export_csv(st.session_state["token"])

            if response.status_code == 200:

                st.download_button(
                    label="⬇ Download flight_log.csv",
                    data=response.content,
                    file_name="flight_log.csv",
                    mime="text/csv",
                )

            else:

                st.error("Unable to generate CSV.")
