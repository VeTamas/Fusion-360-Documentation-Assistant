def find_doc_section(query: str) -> str:
    """
    Returns a hint about which document section likely contains the answer.
    """
    return (
        "Relevant information is likely located in the 'Parametric Modeling' "
        "or 'Design Fundamentals' sections of the Fusion 360 documentation."
    )