import os
import json
import openai
from .base import AIProvider
from ..tools import execute_read_only_query

class OpenAIProvider(AIProvider):
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        openai.api_key = self.api_key
        self.model_name = "gpt-4o"
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute_read_only_query",
                    "description": "Executes a SELECT SQL query against the Afeka College PostgreSQL database.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_query": {
                                "type": "string",
                                "description": "The exact SQL string to execute."
                            }
                        },
                        "required": ["sql_query"]
                    }
                }
            }
        ]

    def ask(self, user_message: str, dynamic_system_instruction: str) -> str:
        messages = [
            {"role": "system", "content": dynamic_system_instruction},
            {"role": "user", "content": user_message}
        ]
        
        client = openai.OpenAI(api_key=self.api_key)
        
        for _ in range(5):
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            messages.append(message)
            
            if not message.tool_calls:
                return message.content or ""
            
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                query_to_run = args.get("sql_query", "")
                
                print(f"[OpenAI] Executing Tool Query: {query_to_run}")
                db_result = execute_read_only_query(query_to_run)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps({"result": db_result})
                })
        
        return "I am having trouble accessing the database right now. Please try again."
