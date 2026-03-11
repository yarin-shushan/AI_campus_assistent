from database import get_session
from sqlmodel import text
import json
import os

def execute_read_only_query(sql_query: str) -> str:
    """
    Executes a SELECT SQL query against the Afeka College PostgreSQL database to retrieve information about students, lecturers, classrooms, courses, exams, or FAQs.
    """
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE", "COMMIT"]
    query_upper = sql_query.upper()
    if any(keyword in query_upper for keyword in forbidden_keywords):
        return "Error: Only read-only (SELECT) queries are allowed."

    try:
        # Use your official get_session generator safely
        session_generator = get_session()
        session = next(session_generator)
        
        try:
            # Note: We must explicitly use sqlmodel.text to wrap the RAW sql string
            result = session.exec(text(sql_query)).fetchall()
            session.rollback()
            if not result:
                return "Query executed successfully. Result: No records found."
            formatted_result = []
            for row in result:
                if hasattr(row, '_mapping'):
                    formatted_result.append(dict(row._mapping))
                elif isinstance(row, tuple):
                     formatted_result.append(list(row))
                else:
                    formatted_result.append(str(row))
            
            # Convert that list into a JSON string safely
            json_result = json.dumps(formatted_result, default=str)
            return f"Query Success. Results: {json_result}"
        finally:
            # Generators for dependencies typically handle closing automatically
            pass
    except StopIteration:
        return "Error: Could not establish a database session."
    except Exception as e:
        return f"Error executing query: {str(e)}"


# Apply the custom Tool Prompt from the environment over the native docstring
# We can do this here or when importing. Let's do it here as requested.
execute_read_only_query.__doc__ = os.environ.get(
    "TOOL_PROMPT", 
    execute_read_only_query.__doc__
).replace('\\n', '\n')
