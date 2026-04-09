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
        
        # Clean DE_translated for matching only
        df["DE_translated"] = df["DE_translated"].astype(str).str.lower().str.strip()
        
        # Keep original FR values (important for accents & caps)
        fr_original = df["FR"].dropna().tolist()
        
        # Create lowercase version for matching
        fr_lower = [str(x).lower().strip() for x in fr_original]

        # Matching function
        def match(text):
            if pd.isna(text):
                return ""
            
            result = process.extractOne(text, fr_lower)
            
            if result and result[1] > 90:
                # Return original FR (preserves accents & capitalization)
                return fr_original[result[2]]
            return ""

        # Apply matching
        df["Matched_FR"] = df["DE_translated"].apply(match)

        st.success("Mapping Completed!")
        st.dataframe(df)

        # FIX: Proper encoding for accents in CSV
        csv = df.to_csv(index=False, encoding="utf-8-sig")

        st.download_button(
            "Download Result",
            csv,
            "mapped_colors.csv",
            "text/csv"
        )
