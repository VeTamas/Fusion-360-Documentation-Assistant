def recommend_workflow(topic: str) -> str:
    """
    Returns a recommended workflow for a Fusion 360 task.
    """
    workflows = {
        "parametric design": (
            "1. Plan your design and key parameters\n"
            "2. Create sketches with parameters\n"
            "3. Define user parameters in Modify > Change Parameters\n"
            "4. Build 3D features based on sketches\n"
            "5. Apply constraints to maintain design intent\n"
            "6. Test and iterate by changing parameters\n"
            "7. Organize timeline for clarity"
        ),
        "assembly modeling": (
            "1. Create individual components\n"
            "2. Activate components\n"
            "3. Use joints to connect components\n"
            "4. Test motion and check for interference\n"
            "5. Apply parameters to critical dimensions if needed"
        ),
        "bracket design": (
            "1. Create base sketch for bracket profile\n"
            "2. Define dimensions using parameters\n"
            "3. Extrude the profile\n"
            "4. Add holes or cutouts with parametric dimensions\n"
            "5. Apply fillets or chamfers\n"
            "6. Test fit with assembly components"
        ),
        "parametric assembly": (
            "1. Define key parameters for components\n"
            "2. Model individual components using parameters\n"
            "3. Assemble components using joints\n"
            "4. Adjust parameters to test fit and motion\n"
            "5. Update features as needed for assembly constraints"
        ),
        "sketching": (
            "1. Start a new sketch on the desired plane\n"
            "2. Draw basic shapes\n"
            "3. Apply dimensions using parameters\n"
            "4. Add constraints to control geometry\n"
            "5. Finish sketch and proceed to features"
        ),
        # további tipikus workflow-k ide jöhetnek...
    }

    return workflows.get(
        topic.lower(),
        ""  # üres, így RAG próbálkozhat először
    )