import tiktoken

# the in-/out-/request price in USD per M-token
# for ours
MODEL_PRICE = {'gpt-4o-mini':   [0.15, 0.6, 0], # [02/20]
                'gpt-4o':        [2.5, 10, 0], # [02/20]
                'gemini-2.0-flash': [0.1, 0.4, 0], # [02/20]
                'gemini-2.0-flash-lite-preview-02-05': [0.075, 0.3, 0], # [02/20]
                'gemini-1.5-pro':    [1.25, 5, 0], # [02/20]
                'llama-3-8B':     [0.03, 0.05, 0], # [02/20] 3.1 @ deepinfra
                'llama-3-70B':    [0.23, 0.4, 0], # [02/20] 3.1 @ deepinfra
                'deepseek-v3':     [0.49, 0.89, 0], # [02/20]
                'phi-4':          [0.07, 0.14, 0], # [02/20]
                'mistral-small':    [0.07, 0.14, 0] # [02/20]
                }

def price_of(input_text, output_text, model):
    # we assume the output size is constantly 1 for classification problems
    assert model in MODEL_PRICE, f'wrong: {model} not supported'
    # we simply apply the tiktoken to count tht token number for all models
    encoding = tiktoken.get_encoding('cl100k_base')
    in_token_num = len(encoding.encode(input_text))
    out_token_num = len(encoding.encode(output_text))
    in_price = MODEL_PRICE[model][0] * in_token_num / 1e6
    out_price = MODEL_PRICE[model][1] * out_token_num / 1e6
    request_price = MODEL_PRICE[model][2]
    return in_price + out_price + request_price

def price_all(q, models):
    costs = []
    for m in models:
        costs.append(price_of(q, m))
    return costs