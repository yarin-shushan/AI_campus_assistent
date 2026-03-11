import pytest
from fastapi.testclient import TestClient
from app.ai_agent import ask_smart_campus
from app.tools.db_tool import execute_read_only_query
from main import app
import time

client = TestClient(app)

def test_execute_read_only_query():
    """
    Test Tool Execution: Verify that the tool can query the DB and find the 'Ficus' building.
    """
    query = "SELECT * FROM building WHERE name = 'Ficus';"
    result = execute_read_only_query(query)
    
    assert "Query Success" in result
    assert "Ficus" in result

def test_llm_tool_invocation():
    """
    Test Agent Tool Invocation: Ask a clear question to verify the LLM uses the SQL tool 
    and returns a helpful response.
    """
    from app.models.user import User
    question = "What is the room number for the Python exam?"
    
    print("[Test] Sleeping for 4 seconds before LLM call to respect rate limits...")
    time.sleep(1)
    
    dummy_user = User(id=1, email="test@test.com", hashed_password="pw", role="admin")
    response = ask_smart_campus(question, dummy_user)
    
    assert isinstance(response, str)
    assert any(word in response for word in ["102", "Ficus", "Python", "classroom", "Ficus 102"])

def test_post_ask_endpoint():
    """
    Test API Endpoint: Send payload to /chat/ask and assert it returns status 200
    with a valid natural language answer.
    """
    payload = {"query": "Is there a Data Structures course?"}
    
    # Mocking authenticated user context
    from app.auth import get_current_user
    from app.models.user import User
    
    def override_get_current_user():
        # יצירת משתמש אדמין זמני לטובת הטסט
        return User(id=1, email="test@test.com", hashed_password="pw", role="admin")
        
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    print("[Test] Sleeping to respect rate limits...")
    time.sleep(1)
    
    response = client.post("/chat/ask", json=payload)
    app.dependency_overrides.clear()
    
    # בדיקה שהסטטוס הוא 200 (הצלחנו להגיע ל-AI)
    assert response.status_code == 200
    
    data = response.json()
    
    # תיקון: אנחנו בודקים שיש שדה 'reply' כי זה מה שה-API מחזיר
    assert "reply" in data
    # בדיקה שה-AI אכן ענה משהו רלוונטי על מבני נתונים
    assert "Data Structures" in data["reply"]