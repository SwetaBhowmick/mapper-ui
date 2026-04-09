import streamlit as st
import pandas as pd
from rapidfuzz import process

st.title("Color Mapping Tool (DE → FR)")

file = st.file_uploader("Upload Excel File", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    st.write("Preview:")
    st.dataframe(df.head())

    if st.button("Run Mapping"):
        
        # Clean text
        df["DE_translated"] = df["DE_translated"].astype(str).str.lower().str.strip()
        df["FR"] = df["FR"].astype(str).str.lower().str.strip()

        fr_list = df["FR"].dropna().tolist()

        # Matching function
        def match(text):
            result = process.extractOne(text, fr_list)
            if result and result[1] > 90:
                return result[0]
            return ""

        df["Matched_FR"] = df["DE_translated"].apply(match)

        st.success("Mapping Completed!")
        st.dataframe(df)

        st.download_button(
            "Download Result",
            df.to_csv(index=False),
            "mapped_colors.csv"
        )
