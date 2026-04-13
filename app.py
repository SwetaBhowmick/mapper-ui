import streamlit as st
import pandas as pd
from rapidfuzz import process

st.title("Mapper UI (US → DE)")

file = st.file_uploader("Upload Excel File", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    st.write("Preview:")
    st.dataframe(df.head())

    if st.button("Run Mapping"):
        
        # Clean US for matching
        df["US_clean"] = df["US"].astype(str).str.lower().str.strip()
        
        # Clean DE_translated for matching
        df["DE_translated_clean"] = df["DE_translated"].astype(str).str.lower().str.strip()
        
        # Keep original DE values (for accents)
        de_original = df["DE"].dropna().tolist()
        
        # Lowercase version for matching
        de_translated_lower = df["DE_translated_clean"].tolist()

        # Matching function
        def match(text):
            if pd.isna(text):
                return ""
            
            result = process.extractOne(text, de_translated_lower)
            
            if result and result[1] > 90:
                # Return original DE (preserves umlauts, accents)
                return de_original[result[2]]
            return ""

        # Apply matching
        df["Mapped_DE"] = df["US_clean"].apply(match)

        st.success("Mapping Completed!")
        st.dataframe(df)

        # Preserve accents in CSV
        csv = df.to_csv(index=False, encoding="utf-8-sig")

        st.download_button(
            "Download Result",
            csv,
            "mapped_us_de.csv",
            "text/csv"
        )
