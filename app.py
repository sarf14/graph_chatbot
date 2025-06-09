import streamlit as st
from query_generator import get_groq_response
from db_utils import execute_sql_query
from nlp_response import get_response_for_query_result
from visualization import generate_dashboard
from visualization import plot_100_percent_stacked_bar_chart
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

st.set_page_config(page_title="Chat with MySQL DB", layout="centered")
st.title("Chat with MySQL Database")

# Month and Transaction Mode choices
MONTH_CHOICES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
TRANSACTION_MODES = ["FACEPAY", "UPI", "CASH"]

# Updated Prompt Templates with placeholders
PROMPTS = {
    "Daily transaction mode for All ATM's":
        "Give me an elaborate line chart for daily {modes} transaction mode for all atm ids together for months {months} each line should represent distinct trnasaction modes",

    "FACEPAY daily for MUPI0008, MUPI0009, MUPI0016":
        "give me a elaborate line chart for number of daily {modes} mode transaction for EACH of the following atm id {atm1}, {atm2}, {atm3}, {atm4}, {atm5} for  every days in month {months}",
    
    "Bar chart":
        "Generate a query that returns daily transaction counts broken down by status. The result should include: - `date` (in `YYYY-MM-DD` format) - `status` (transaction status like 'Transaction Success', 'Transaction Timeout', etc.) - `count` (number of transactions for that status on that day) This will be used to create a 100% stacked bar chart showing the proportion of each transaction status for each day in the month of {months}. The chart should show each status as a segment in the bar, and the entire bar for each day should sum to 100% only. Make sure the SQL result returns three columns: `date`, `status`, `count`.",

    "Weekwise transaction trend":
        "give me a line chart for count of {modes} transaction modes for every 7 days in {months} for  each of the atm id {atm1},{atm2},{atm3},{atm4} and {atm5},name every group of sevenday as 1, 2 and so on and remaining days as 5"
}

# Session state for history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Select template
selected_prompt = st.selectbox("Choose a Query Template", list(PROMPTS.keys()))

# Form input section
with st.form("template_form"):
    final_question = ""

    # ATM input
    if "atm_id" in PROMPTS[selected_prompt]:
        atm_id = st.text_input("Enter ATM ID", value="MUPI0008")
        
    if "{atm1}" in PROMPTS[selected_prompt]:
        atm1 = st.text_input("ATM 1", value="MUPI0008")
        atm2 = st.text_input("ATM 2", value="MUPI0009")
        atm3 = st.text_input("ATM 3", value="MUPI")
        atm4 = st.text_input("ATM 4", value="MUPI")
        atm5 = st.text_input("ATM 5", value="MUPI")
    # Month selection
    selected_months = st.multiselect("Select up to 3 Months", MONTH_CHOICES, max_selections=3)

    # Transaction mode selection
    selected_modes = st.multiselect("Select 1 to 3 Transaction Modes", TRANSACTION_MODES)

    submit = st.form_submit_button("Run")

    if submit:
        if not selected_months:
            st.warning("Please select at least one month.")
        elif not selected_modes:
            st.warning("Please select at least one transaction mode.")
        else:
            month_string = ", ".join(selected_months)
            mode_string = ", ".join(selected_modes)
            final_question = PROMPTS[selected_prompt].format(
                atm_id=atm_id if 'atm_id' in locals() else '',
                atm1=atm1 if 'atm1' in locals() else '',
                atm2=atm2 if 'atm2' in locals() else '',
                atm3=atm3 if 'atm3' in locals() else '',
                atm4=atm4 if 'atm4' in locals() else '',
                atm5=atm5 if 'atm5' in locals() else '',
                months=month_string,
                modes=mode_string
            )

            st.write(f"**Final Query:** {final_question}")

            # Get SQL from LLM
            query = get_groq_response(final_question)
            st.write(f"**Generated SQL:** `{query}`")

            # Run SQL
            data = execute_sql_query(query)

            if isinstance(data, str):
                st.error(data)
            elif data.empty:
                st.warning("No data found for this query.")
            else:
                if any(kw in final_question.lower() for kw in ["chart", "bar", "line"]):
                      st.subheader("Generated Dashboard(s):")

                if selected_prompt == "Bar chart":
                    required_columns = {"date", "status", "count"}
                    if not required_columns.issubset(set(data.columns)):
                        st.error("The SQL result must include 'date', 'status', and 'count' columns for the bar chart.")
                    else:
                        plot_100_percent_stacked_bar_chart(data)
                else:
                    generate_dashboard(data,final_question,selected_prompt)


# Sidebar: DB config
with st.sidebar:
    st.title("🔗 Connect to Database")
    st.text_input("Host", key="host", value=DB_HOST)
    st.text_input("Port", key="port", value=DB_PORT)
    st.text_input("Username", key="username", value=DB_USER)
    st.text_input("Password", key="password", type="password", value=DB_PASSWORD)
    st.text_input("Database", key="database", value=DB_NAME)

    if st.button("Connect"):
        st.success("Database connection values updated!")
