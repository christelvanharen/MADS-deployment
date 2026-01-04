"""
Simple DNA to RNA converter utility
"""


def dna_to_rna(dna_sequence: str) -> str:
    """
    Convert DNA sequence to RNA sequence.
    
    Replaces Thymine (T) with Uracil (U).
    
    Args:
        dna_sequence: DNA sequence string (A, T, C, G)
    
    Returns:
        RNA sequence string (A, U, C, G)
    
    Raises:
        ValueError: If invalid bases are present
    """
    # Clean and convert to uppercase
    rna = dna_sequence.upper().replace(" ", "").replace("\n", "")
    
    # Validate
    valid_bases = set("ATCG")
    if not all(base in valid_bases for base in rna):
        invalid = set(rna) - valid_bases
        raise ValueError(f"Invalid DNA bases: {invalid}. Only A, T, C, G allowed.")
    
    # Convert T to U
    rna = rna.replace("T", "U")
    
    return rna


def reverse_complement(dna_sequence: str) -> str:
    """
    Get reverse complement of DNA sequence.
    
    Args:
        dna_sequence: DNA sequence string
    
    Returns:
        Reverse complement sequence
    """
    complement_map = {"A": "T", "T": "A", "C": "G", "G": "C"}
    dna_clean = dna_sequence.upper().replace(" ", "").replace("\n", "")
    
    # Validate
    valid_bases = set("ATCG")
    if not all(base in valid_bases for base in dna_clean):
        raise ValueError("Invalid DNA bases. Only A, T, C, G allowed.")
    
    complement = "".join(complement_map[base] for base in dna_clean)
    return complement[::-1]


if __name__ == "__main__":
    # Test examples
    test_dna = "ATCGATCG"
    print(f"DNA: {test_dna}")
    print(f"RNA: {dna_to_rna(test_dna)}")
    print(f"Reverse complement: {reverse_complement(test_dna)}")
