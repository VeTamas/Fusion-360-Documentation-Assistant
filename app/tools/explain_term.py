def explain_term(term: str) -> str:
    """
    Returns a short, clear explanation of a Fusion 360 term.
    """
    explanations = {
        "parametric design": (
            "Parametric design in Fusion 360 is a modeling approach where "
            "geometry is driven by parameters and constraints, allowing "
            "design changes to automatically propagate through the model."
        ),
        "timeline": (
            "The timeline in Fusion 360 records the sequence of modeling "
            "operations, enabling users to edit features at any point."
        ),
        "feature history": (
            "Feature history records all the steps used to create a model. "
            "Each feature can be edited later, and changes propagate automatically."
        ),
        "sketch constraints": (
            "Sketch constraints in Fusion 360 define geometric relationships "
            "between sketch elements, ensuring predictable behavior when dimensions change."
        ),
        "user parameters": (
            "User parameters are custom variables defined in Fusion 360 "
            "that control dimensions or other values in the model, allowing easy updates."
        ),
        "design intent": (
            "Design intent refers to the intended behavior of a model when "
            "changes are made, achieved through parameters and constraints."
        ),
        # ide lehet még több Fusion 360 kulcsszót felvenni...
    }

    return explanations.get(
        term.lower(),
        ""  # üres string, hogy RAG / LLM fallback próbálkozhasson
    )