import os
from .providers.gemini_provider import GeminiProvider
from .providers.openai_provider import OpenAIProvider

DB_SCHEMA = os.environ.get("DB_SCHEMA", "").replace('\\n', '\n')
RAW_SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", "").replace('\\n', '\n')
SYSTEM_INSTRUCTION = RAW_SYSTEM_PROMPT.replace("{DB_SCHEMA}", DB_SCHEMA)

def get_ai_provider():
    provider_name = os.environ.get("AI_PROVIDER", "gemini").lower()
    if provider_name == "openai":
        return OpenAIProvider()
    return GeminiProvider()

def ask_smart_campus(user_message: str, current_user) -> str:
    """Main orchestration function that delegates to the configured AI provider."""
    try:
        # Determine the user's role and build the User Context
        if current_user.role == 'admin':
            role_prompt = "USER CONTEXT: You are interacting with an Admin. You have unrestricted read access to query data for all students and lecturers in the database."
        else:
            if current_user.role == 'student' and getattr(current_user, 'student_profile', None):
                full_name = current_user.student_profile.full_name
            elif current_user.role == 'lecturer' and getattr(current_user, 'lecturer_profile', None):
                full_name = current_user.lecturer_profile.full_name
            else:
                full_name = current_user.email
                
            role_prompt = f"USER CONTEXT: You are interacting with a {current_user.role} named {full_name} (Database ID: {current_user.id}). PRIVACY RULE: You MUST ONLY query and return personal information belonging to this specific user. If the user asks for grades, schedules, or personal details of OTHER students or lecturers, politely refuse and state you are only authorized to access their own data. When executing SQL queries for their personal data, you must explicitly filter by their ID."

        dynamic_system_instruction = f"{role_prompt}\n\n{SYSTEM_INSTRUCTION}"
        
        provider = get_ai_provider()
        return provider.ask(user_message, dynamic_system_instruction)

    except Exception as e:
        return f"I'm sorry, I'm currently having trouble processing that request. (Error: {str(e)})"
