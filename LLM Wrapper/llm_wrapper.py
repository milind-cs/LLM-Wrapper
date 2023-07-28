import time
import openai

class LLMWrapper:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
        self.conversation_history = []

    def add_to_conversation(self, role, content):
        # Add the message to the conversation history
        self.conversation_history.append({"role": role, "content": content})

    def generate_prompt(self, variables):
        # Format the conversation history and variables into a prompt
        prompt = ""
        for variable in variables:
            prompt += f"{variable['name']}: {variable['value']}\n"
        for message in self.conversation_history:
            prompt += message['role'] + ": " + message['content'] + "\n"
        return prompt

    def call_llm(self, messages):
    # Call the LLM with the given messages
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
        except openai.error.RateLimitError:
            # If a rate limit error occurs, wait for a second and then try again
            time.sleep(1)
            response = self.call_llm(messages)
        return response


    def get_response(self, user_input, variables):
        # Add the user's input to the conversation history
        self.add_to_conversation("user", user_input)

        # Generate a prompt from the conversation history and variables
        prompt = self.generate_prompt(variables)

        # If the prompt is too long, remove the oldest messages until it's short enough
        while len(prompt) > 4096:
            self.conversation_history.pop(0)
            prompt = self.generate_prompt(variables)

        # Prepare the messages for the chat model
        messages = [{"role": message["role"], "content": message["content"]} for message in self.conversation_history]

        # Call the LLM with the messages
        response = self.call_llm(messages)

        # Add the LLM's response to the conversation history
        self.add_to_conversation("assistant", response['choices'][0]['message']['content'])

        return response['choices'][0]['message']['content']


