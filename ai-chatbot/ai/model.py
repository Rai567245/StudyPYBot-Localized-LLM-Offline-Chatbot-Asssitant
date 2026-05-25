import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread

class StudyPYModel:
    def __init__(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_id = model_id
        self.device = "cpu" 
        
        print(f"Loading StudyPYBot (Python Specialist Mode)...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float32, 
            low_cpu_mem_usage=True      
        ).to(self.device)               

    def generate_streaming_response(self, user_input, history=""):
        # We refined the instruction to be even more strict about 'Study Guides'
        # so it doesn't default to writing random scripts for simple greetings.
        system_instruction = (
            "You are StudyPYBot, a specialized Python Tutor. "
            "Your ONLY goal is to provide Python Study Guides. "
            "If the user says 'Hello' or 'Hi', respond with: 'Hello! I am StudyPYBot. How can I help you with Python today?' "
            "STRICT RULES: 1. Only discuss Python. 2. Keep responses direct. "
            "3. Structure: Concept -> Definition -> 2-question Quiz."
        )

        # Updated Prompt Format to better separate System, User, and Assistant
        prompt = f"<|system|>\n{system_instruction}</s>\n<|user|>\n{history}\n{user_input}</s>\n<|assistant|>\n"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

        generation_kwargs = dict(
            input_ids=inputs["input_ids"],
            streamer=streamer,
            max_new_tokens=500, 
            do_sample=False, # Keeping it False ensures consistent answers
            repetition_penalty=1.2,
            use_cache=True,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id 
        )
        
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        # Stop words to prevent the AI from generating extra junk
        stop_words = ["<|user|>", "Script:", "User:"]

        for new_text in streamer:
            # If the model tries to hallucinate a new user turn or 'Script:', stop it.
            if any(stop in new_text for stop in stop_words):
                break
            yield new_text