import json
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Turkey 2008 HDR Dashboard",
    layout="wide"
)

OUTPUT_DIR = Path("outputs")

st.title("Turkey 2008 Human Development Report Dashboard")
st.write("Local LLM PDF-to-Dashboard Pipeline")


def load_csv(filename):
    path = OUTPUT_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def load_text(filename):
    path = OUTPUT_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "File not found."


def load_json(filename):
    path = OUTPUT_DIR / filename
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


theme_df = load_csv("theme_counts.csv")
indicator_df = load_csv("manual_indicators.csv")
numbers_df = load_csv("numbers_and_years.csv")
chapter_df = load_csv("chapter_summaries.csv")
model_df = load_csv("model_comparison.csv")
strengths_df = load_csv("strengths_challenges.csv")

key_findings = load_text("key_findings.txt")
evaluation = load_text("llm_evaluation.txt")

indicators_json = load_json("clean_indicators.json")
chunks_json = load_json("text_chunks.json")
dashboard_json = load_json("dashboard_data.json")


st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Key Findings",
        "Themes",
        "Indicators",
        "Chunks",
        "JSON Output",
        "Chapters",
        "Strengths & Challenges",
        "Model Evaluation",
        "Extracted Data"
    ]
)


if page == "Overview":
    st.header("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Country", indicators_json.get("country", "Turkey"))
    col2.metric("Report Year", indicators_json.get("report_year", "2008"))
    col3.metric("Youth Population", str(indicators_json.get("youth_population_million", "N/A")) + "M")
    col4.metric("Youth Share", str(indicators_json.get("youth_share_percent", "N/A")) + "%")

    st.subheader("Report Theme")
    st.info(indicators_json.get("report_theme", "Youth in Turkey"))

    st.subheader("Dashboard Purpose")
    st.write(
        "This dashboard presents structured outputs extracted from the Turkey 2008 Human Development Report "
        "using a local LLM PDF pipeline. It includes key findings, themes, indicators, chunks, JSON outputs, "
        "chapter summaries, strengths, challenges, and model evaluation."
    )


elif page == "Key Findings":
    st.header("Key Findings")
    st.markdown(key_findings)


elif page == "Themes":
    st.header("Theme Analysis")

    if not theme_df.empty:
        st.dataframe(theme_df, use_container_width=True)

        fig = px.bar(
            theme_df,
            x="theme",
            y="keyword_count",
            title="Theme Keyword Frequency",
            text="keyword_count"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("theme_counts.csv not found.")


elif page == "Indicators":
    st.header("Extracted Indicators")

    if not indicator_df.empty:
        st.dataframe(indicator_df, use_container_width=True)

        numeric_df = indicator_df.copy()
        numeric_df["value_numeric"] = pd.to_numeric(numeric_df["value"], errors="coerce")
        numeric_df = numeric_df.dropna(subset=["value_numeric"])

        fig = px.bar(
            numeric_df,
            x="value_numeric",
            y="indicator",
            orientation="h",
            title="Selected Numerical Indicators"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("manual_indicators.csv not found.")

    st.subheader("Raw Indicator JSON")
    st.json(indicators_json)


elif page == "Chunks":
    st.header("Text Chunks")

    if chunks_json:
        chunks_df = pd.DataFrame(chunks_json)

        st.write("These are the text chunks created from the cleaned PDF text before sending to the LLM.")
        st.metric("Total Chunks", len(chunks_df))

        st.dataframe(chunks_df, use_container_width=True)

        selected_chunk = st.selectbox(
            "Select a chunk to view full text",
            chunks_df["chunk_id"].tolist()
        )

        selected_text = chunks_df[chunks_df["chunk_id"] == selected_chunk]["text"].iloc[0]

        st.subheader(f"Chunk {selected_chunk} Text")
        st.text_area("Chunk text", selected_text, height=350)

    else:
        st.warning("text_chunks.json not found.")


elif page == "JSON Output":
    st.header("JSON Outputs")

    st.subheader("Clean Indicators JSON")
    st.json(indicators_json)

    st.subheader("Text Chunks JSON")
    if chunks_json:
        st.json(chunks_json[:3])
        st.info("Showing first 3 chunks only to keep the dashboard readable.")
    else:
        st.warning("text_chunks.json not found.")

    st.subheader("Dashboard Data JSON")
    if dashboard_json:
        st.json(dashboard_json)
    else:
        st.warning("dashboard_data.json not found.")


elif page == "Chapters":
    st.header("Chapter Summaries")

    if not chapter_df.empty:
        for _, row in chapter_df.iterrows():
            with st.expander(row["chapter"]):
                st.write(f"Pages: {row['start_page']} - {row['end_page']}")
                st.write(row["summary"])
    else:
        st.warning("chapter_summaries.csv not found.")


elif page == "Strengths & Challenges":
    st.header("Strengths & Challenges")

    if not strengths_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Strengths")
            for item in strengths_df["strengths"].dropna():
                st.success(item)

        with col2:
            st.subheader("Challenges")
            for item in strengths_df["challenges"].dropna():
                st.error(item)
    else:
        st.warning("strengths_challenges.csv not found.")


elif page == "Model Evaluation":
    st.header("Model Comparison and Evaluation")

    if not model_df.empty:
        st.subheader("Model Comparison Table")
        st.dataframe(model_df, use_container_width=True)

        score_cols = [
            col for col in model_df.columns
            if "score" in col.lower()
        ]

        if score_cols:
            model_score_df = model_df.melt(
                id_vars="model",
                value_vars=score_cols,
                var_name="metric",
                value_name="score"
            )

            fig = px.bar(
                model_score_df,
                x="model",
                y="score",
                color="metric",
                barmode="group",
                title="Local LLM Model Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("LLM Evaluation")
    st.write(evaluation)


elif page == "Extracted Data":
    st.header("Extracted Data Files")

    st.subheader("Numbers and Years")
    if not numbers_df.empty:
        st.dataframe(numbers_df, use_container_width=True)
    else:
        st.warning("numbers_and_years.csv not found.")

    st.subheader("Indicators")
    if not indicator_df.empty:
        st.dataframe(indicator_df, use_container_width=True)

    st.subheader("Themes")
    if not theme_df.empty:
        st.dataframe(theme_df, use_container_width=True)