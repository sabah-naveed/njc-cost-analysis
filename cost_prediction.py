MODEL_PRICING = {
    "gpt-4o-mini": {
        "input_per_1M": 0.15,
        "cache_per_1M": 0.075,
        "output_per_1M": 0.60,
    },
    "gpt-4o": {
        "input_per_1M": 2.50,
        "cache_per_1M": 1.25,
        "output_per_1M": 10.00,
    },
    
}

MODEL_PRICING_LINK = "https://platform.openai.com/docs/pricing"

def calculate_cost(model, input_tokens, output_tokens, cache_tokens):
    prices = MODEL_PRICING.get(model, {})
    if not prices:
        print("could not get prices for model: ", model)
        return None
    
    cost_input = (input_tokens / 1000000) * prices["input_per_1M"]
    cost_output = (output_tokens / 1000000) * prices["output_per_1M"]
    cost_cache = (cache_tokens / 1000000) * prices["cache_per_1M"]

    total_cost = cost_input + cost_output + cost_cache
    return total_cost

def main():
    model = "gpt-4o-mini"
    