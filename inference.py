import os
from tokenizers import Tokenizer
import ctranslate2


def generate_response_ctranslate2(prompt, model_folder):
    # Tokenize the input
    tokenizer = Tokenizer.from_file(os.path.join(model_folder, "tokenizer.json"))
    input_tokens = tokenizer.encode(prompt).tokens

    model_base_path = model_folder

    # Initialize the translator
    model = ctranslate2.Translator(model_base_path, compute_type="int8")

    # Translate the tokens
    results = model.generate_tokens(input_tokens, disable_unk=True)

    accumlated_results = []
    current_length = 0
    for item in results:
        if item.is_last:
            break
        accumlated_results.append(item.token_id)
        decoded_string = tokenizer.decode(accumlated_results)
        new_text = decoded_string[current_length - len(decoded_string) :]
        current_length = len(decoded_string)
        yield new_text
