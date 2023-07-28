from llm_wrapper import LLMWrapper

llm = LLMWrapper("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")
variables = [{"name": "variable1", "value": "value1"}, {"name": "variable2", "value": "value2"}]
response = llm.get_response("Hello, how are you?", variables)
print(response)
