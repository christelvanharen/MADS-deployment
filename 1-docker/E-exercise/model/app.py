import streamlit as st

st.set_page_config(page_title="DNA to RNA Converter", layout="centered")

st.title("🧬 DNA to RNA Converter")

st.markdown("""
A simple educational tool to convert DNA sequences to RNA sequences.

**How it works:**
- Replace all Thymine (T) with Uracil (U)
- Keep Adenine (A), Guanine (G), and Cytosine (C) unchanged
""")

st.divider()

# Input
dna_sequence = st.text_area(
    "Enter DNA sequence:",
    placeholder="e.g., ATCGATCG",
    height=100
)

if dna_sequence:
    # Clean and convert
    dna_clean = dna_sequence.upper().replace(" ", "").replace("\n", "")
    
    # Validate
    valid_bases = set("ATCG")
    if all(base in valid_bases for base in dna_clean):
        # Convert to RNA
        rna_sequence = dna_clean.replace("T", "U")
        
        st.success("✅ Valid DNA sequence")
        
        st.markdown("### RNA Output:")        
        # Statistics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Length", len(rna_sequence))
        st.code(rna_sequence, language="text")
    else:
        st.error("❌ Invalid DNA sequence. Only use A, T, C, G characters.")
