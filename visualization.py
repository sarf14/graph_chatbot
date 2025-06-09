import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pandasai import SmartDataframe
from config import llm
import pandas as pd
import io
import plotly.express as px
import plotly.graph_objects as go

def plot_100_percent_stacked_bar_chart(data: pd.DataFrame):
    required_columns = ['date', 'status', 'count']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"❌ Required columns missing: {', '.join(missing_columns)}.\nPlease ensure your SQL query returns: {', '.join(required_columns)}")
        return

    # Ensure correct types
    data['date'] = pd.to_datetime(data['date'])
    data['count'] = pd.to_numeric(data['count'], errors='coerce').fillna(0)
    data['status'] = data['status'].astype(str).str.strip().str.title()

    # Aggregate counts per date and status
    daily_status_counts = data.groupby(['date', 'status'])['count'].sum().reset_index()

    # Calculate total transactions per date
    daily_totals = daily_status_counts.groupby('date')['count'].sum().reset_index().rename(columns={'count': 'total_count'})

    # Merge to compute percentage per status
    merged = pd.merge(daily_status_counts, daily_totals, on='date')
    merged['percentage'] = (merged['count'] / merged['total_count']) * 100

    # Optional debug view
    with st.expander("🛠 Debug Data"):
        st.dataframe(merged)

    # Plot
    fig = px.bar(
        merged,
        x='date',
        y='percentage',
        color='status',
        title="📊 100% Stacked Bar Chart of Transaction Status by Day",
        labels={"percentage": "Percentage (%)", "date": "Date", "status": "Transaction Status"},
        text_auto=".2f"
    )
    fig.update_layout(
        barmode='stack',
        xaxis={'categoryorder': 'category ascending'},
        yaxis=dict(title="Percentage of Daily Transactions", tickformat=".0f")
    )
    st.plotly_chart(fig, use_container_width=True)

def generate_dashboard(data, question, prompt: str):
    prompt_lower = prompt.lower()

    st.write("### 📄 Data Preview:")
    st.dataframe(data)

    # Check for 100% stacked bar chart request
    if "100% stacked bar" in prompt_lower or "bar chart" in prompt_lower:
        plot_100_percent_stacked_bar_chart(data)

    st.write("### 📊 Generated Chart (via PandasAI):")

    # Normalize input to DataFrame
    if isinstance(data, list):
        data = pd.DataFrame(data)
    elif not isinstance(data, pd.DataFrame):
        data = pd.DataFrame([data])

    try:
        smart_df = SmartDataframe(data, config={
            "llm": llm,
            "verbose": True,
            "enable_safety_guardrails": False,
            "save_charts": False,
            "show_charts": True
        })

        with st.spinner("🧠 Asking PandasAI to generate a chart..."):
            result = smart_df.chat(question)

        if isinstance(result, str) and result.strip().startswith("Python"):
            result = result.replace("Python", "", 1).strip()

        st.write("PandasAI Output:")
        st.code(str(result), language="python")

        # Display matplotlib figure if any
        fig = plt.gcf()
        if fig and fig.axes and any(ax.has_data() for ax in fig.axes):
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.image(buf)
            plt.close(fig)
            st.success("✅ Chart generated successfully!")
        else:
            st.warning("⚠️ No chart generated. Retrying...")

            fallback_prompt = f"Plot a simple line chart using only these columns: {', '.join(data.columns)}"
            result = smart_df.chat(fallback_prompt)

            if isinstance(result, str) and result.strip().startswith("Python"):
                result = result.replace("Python", "", 1).strip()

            st.code(str(result), language="python")

            fig = plt.gcf()
            if fig and fig.axes and any(ax.has_data() for ax in fig.axes):
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                st.image(buf)
                plt.close(fig)
                st.success("✅ Chart generated on retry!")
            else:
                st.error("❌ Still no chart after retry. Please double-check column names.")

    except Exception as e:
        st.error(f"❌ Chart generation failed: {e}")
