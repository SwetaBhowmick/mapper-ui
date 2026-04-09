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
        
        # Clean DE_translated for matching ONLY
        df["DE_translated"] = df["DE_translated"].astype(str).str.lower().str.strip()
        
        # Keep original FR values (IMPORTANT)
        fr_original = df["FR"].dropna().tolist()
        
        # Create lowercase version for matching
        fr_lower = [str(x).lower().strip() for x in fr_original]

        # Matching function
        def match(text):
            result = process.extractOne(text, fr_lower)
            if result and result[1] > 90:
                # Return ORIGINAL FR (preserves accents & caps)
                return fr_original[result[2]]
            return ""

        df["Matched_FR"] = df["DE_translated"].apply(match)

        st.success("Mapping Completed!")
        st.dataframe(df)

        st.download_button(
            "Download Result",
            df.to_csv(index=False),
            "mapped_colors.csv"
        )
