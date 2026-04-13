import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

st.title("Mapper UI (US → DE)")

file = st.file_uploader("Upload Excel File", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    st.write("Preview:")
    st.dataframe(df.head())

    if st.button("Run Mapping"):
        
        # Clean columns
        df["US_clean"] = df["US"].astype(str).str.lower().str.strip()
        df["DE_translated_clean"] = df["DE_translated"].astype(str).str.lower().str.strip()
        
        # Keep original DE (for output)
        de_original = df["DE"].dropna().tolist()
        
        # Lower version for matching
        de_translated_lower = df["DE_translated_clean"].tolist()

        # Matching function
        def match(text):
            if pd.isna(text):
                return ""
            
            result = process.extractOne(
                text,
                de_translated_lower,
                scorer=fuzz.token_sort_ratio
            )
            
            if result and result[1] > 90:
                return de_original[result[2]]
            return ""

        # Apply mapping
        df["Mapped_DE"] = df["US_clean"].apply(match)

        st.success("Mapping Completed!")
        st.dataframe(df)

        # Download
        csv = df.to_csv(index=False, encoding="utf-8-sig")

        st.download_button(
            "Download Result",
            csv,
            "mapped_us_de.csv",
            "text/csv"
        )
