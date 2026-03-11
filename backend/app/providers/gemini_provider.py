import os
import json
import google.generativeai as genai
from .base import AIProvider
from ..tools import execute_read_only_query

class GeminiProvider(AIProvider):
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
        genai.configure(api_key=self.api_key)
        self.model_name = "gemini-flash-latest"

    def ask(self, user_message: str, dynamic_system_instruction: str) -> str:
        dynamic_model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=dynamic_system_instruction,
            tools=[execute_read_only_query]
        )
        
        chat = dynamic_model.start_chat()
        response = chat.send_message(user_message)
        
        for _ in range(5):
            fn = None
            if response.parts:
                for part in response.parts:
                    if getattr(part, "function_call", None) and part.function_call.name:
                        fn = part.function_call
                        break
            
            if fn:
                if hasattr(fn.args, "items"):
                    args = {key: val for key, val in fn.args.items()}
                else:
                    args = dict(fn.args)
                    
                query_to_run = args.get("sql_query", "")
                print(f"[Gemini] Executing Tool Query: {query_to_run}")
                
                db_result = execute_read_only_query(query_to_run)
                
                function_response_part = genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=fn.name,
                        response={"result": db_result}
                    )
                )
                
                response = chat.send_message(function_response_part)
            else:
                break
                
        try:
            if response.text:
                return response.text
        except ValueError:
            pass
            
        return "I am having trouble accessing the database right now. Please try again."
