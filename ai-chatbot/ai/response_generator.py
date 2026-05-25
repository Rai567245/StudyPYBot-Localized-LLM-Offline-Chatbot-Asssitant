from ai.model import AIModel

class ResponseGenerator:
    def __init__(self):
        self.model = AIModel()

    def get_response(self, user_input, history):
        return self.model.generate_response(user_input, history)