import json
import os
import time
import string
from ai.model import StudyPYModel
from memory.storage import ChatStorage

class ChatController:
    def __init__(self):
        # Initialize the AI Model and Storage handlers
        self.model = StudyPYModel()
        self.storage = ChatStorage()
        
        # Path to your configuration file
        self.config_path = os.path.join('data', 'config.json')
        
        # Load the Knowledge Base (Pre-prepared responses)
        self.knowledge_base = self.load_kb()

    def load_kb(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    kb_data = data.get("knowledge_base", {})
                    
                    # Merge greetings and concepts into one dictionary
                    greetings = kb_data.get("casual_greetings", {})
                    concepts = kb_data.get("python_concepts", {})
                    
                    # Combine them
                    combined_kb = {**greetings, **concepts}
                    
                    # Clean the keys for matching
                    return {
                        k.lower().translate(str.maketrans('', '', string.punctuation)): v 
                        for k, v in combined_kb.items()
                    }
            return {}
        except Exception as e:
            print(f"Error loading KB: {e}")
            return {}

    def get_streaming_response(self, user_input):
        """Processes user input using Knowledge Base first, then AI Fallback."""
        
        # 1. CLEAN INPUT: Remove punctuation and lowercase to match KB keys
        clean_input = user_input.lower().translate(str.maketrans('', '', string.punctuation)).strip()
        
        # 2. PRIORITY CHECK: Is this a prepared greeting or standard question?
        for key, answer in self.knowledge_base.items():
            # Check if the keyword (e.g., 'hello') is inside the user's message
            if key in clean_input:
                # Save the interaction to conversations.json
                self.storage.save_chat(user_msg=user_input, bot_msg=answer)
                
                # Stream the prepared answer to keep the GUI feeling responsive
                words = answer.split(' ')
                for i, word in enumerate(words):
                    yield word + (" " if i < len(words) - 1 else "")
                    time.sleep(0.01) # Small delay to simulate typing
                
                # CRITICAL: Return stops the function so the AI model is NEVER triggered
                return 

        # 3. AI FALLBACK: Runs only if no Knowledge Base match is found
        # Load the last 3 messages for context to stay within 8GB RAM limits
        context = self.storage.get_recent_history(limit=3)
        
        full_response = ""
        # Get chunks from TinyLlama
        for chunk in self.model.generate_streaming_response(user_input, context):
            full_response += chunk
            yield chunk
            
        # Save the AI-generated guide to history
        self.storage.save_chat(user_input, full_response)

    def export_history(self):
        """Triggers the .txt export feature in the storage class."""
        self.storage.export_to_txt()