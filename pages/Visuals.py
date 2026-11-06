# This creates the page for displaying data visualizations.
import streamlit as st
import json
import pandas as pd
import altair as alt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
with open("data.json", "r") as file:
    data = json.load(file)

st.header(data["chart_title"])
st.write(data["data_source"])

df = pd.DataFrame(data["data_points"])
st.dataframe(df)

st.subheader("Number of Pieces in Each LEGO Project")
st.bar_chart(df, x="label", y="pieces")

st.subheader("Explore LEGO Projects by Theme")

if "selected_theme" not in st.session_state:
    st.session_state["selected_theme"] = "All"

st.selectbox(
    "Choose a theme:",
    ["All", "Architecture", "Rollercoaster", "Space"],
    key="selected_theme"
)

if st.session_state["selected_theme"] == "All":
    filtered_df = df
else:
    filtered_df = df[df["theme"] == st.session_state["selected_theme"]]

st.dataframe(filtered_df)

chart = alt.Chart(filtered_df).mark_circle(size=100).encode(
    x=alt.X("pieces:Q", title="Number of Pieces"),
    y=alt.Y("price:Q", title="Price (USD)"),
    color=alt.Color("theme:N", title="Theme"),
    tooltip=["label", "theme", "pieces", "price"]
).properties(
    title="LEGO Project Price vs. Number of Pieces"
)

st.altair_chart(chart, use_container_width=True)

# Extra Credit: JSON statistics
json_mean = filtered_df["price"].mean()
json_median = filtered_df["price"].median()

if "previous_json_mean" not in st.session_state:
    st.session_state["previous_json_mean"] = json_mean
    st.session_state["previous_json_median"] = json_median

st.write("Price statistics in USD. Changes are compared with the previous display.")

st.metric(
    "Mean price (JSON)",
    round(json_mean, 2),
    delta=round(json_mean - st.session_state["previous_json_mean"], 2),
    delta_color="off"
)

st.metric(
    "Median price (JSON)",
    round(json_median, 2),
    delta=round(json_median - st.session_state["previous_json_median"], 2),
    delta_color="off"
)

st.session_state["previous_json_mean"] = json_mean
st.session_state["previous_json_median"] = json_median

# PART 2: GRAPHS FROM data.csv
st.divider()
st.header("LEGO Projects from the Survey")
st.write("These are fictional practice entries submitted through the survey.")

csv_df = pd.read_csv("data.csv")

st.subheader("Price of Each Submitted LEGO Project")
st.bar_chart(csv_df, x="project_name", y="price")

st.subheader("Explore Submitted Projects by Theme")

if "csv_theme" not in st.session_state:
    st.session_state["csv_theme"] = "All"

st.selectbox(
    "Choose a theme for the survey data:",
    ["All", "Architecture", "Rollercoaster", "Space"],
    key="csv_theme"
)

if st.session_state["csv_theme"] == "All":
    filtered_csv = csv_df
else:
    filtered_csv = csv_df[csv_df["theme"] == st.session_state["csv_theme"]]

csv_chart = alt.Chart(filtered_csv).mark_circle(size=100).encode(
    x=alt.X("pieces:Q", title="Number of Pieces"),
    y=alt.Y("price:Q", title="Price (USD)"),
    color=alt.Color("theme:N", title="Theme"),
    tooltip=["project_name", "theme", "pieces", "price"]
).properties(
    title="Submitted LEGO Projects: Price vs. Number of Pieces"
)

st.altair_chart(csv_chart, use_container_width=True)

# Extra Credit: CSV statistics
if not filtered_csv.empty:
    csv_mean = filtered_csv["price"].mean()
    csv_median = filtered_csv["price"].median()

    if "previous_csv_mean" not in st.session_state:
        st.session_state["previous_csv_mean"] = csv_mean
        st.session_state["previous_csv_median"] = csv_median

    st.write("Price statistics in USD. Changes are compared with the previous display.")

    st.metric(
        "Mean price (CSV)",
        round(csv_mean, 2),
        delta=round(csv_mean - st.session_state["previous_csv_mean"], 2),
        delta_color="off"
    )

    st.metric(
        "Median price (CSV)",
        round(csv_median, 2),
        delta=round(csv_median - st.session_state["previous_csv_median"], 2),
        delta_color="off"
    )

    st.session_state["previous_csv_mean"] = csv_mean
    st.session_state["previous_csv_median"] = csv_median
else:
    st.info("No survey entries for this theme yet.")

