MODEL_PRICES = {
    "gpt-4.1-mini": {
        "prompt": 0.00015 / 1000,
        "completion": 0.0006 / 1000,
    },
}

def calculate_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
):
    if model not in MODEL_PRICES:
        return 0.0

    prices = MODEL_PRICES[model]

    cost = (
        prompt_tokens * prices["prompt"]
        + completion_tokens * prices["completion"]
    )

    return round(cost, 6)