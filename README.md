# 🎓 Smart Campus Assistant - Afeka College

An intelligent full-stack system designed to assist students at Afeka College. The system features an AI-powered agent capable of understanding natural language and interacting directly with campus databases to provide real-time information about courses, classrooms, and student data.

---

## 🚀 Overview

The **Smart Campus Assistant** acts as a bridge between the student and complex campus systems. Instead of searching through portals, students can simply ask: *"What courses am I registered for?"* or *"Are there any free classrooms in Building Mitchell?"*.

### Key Features:
* **Natural Language Processing**: Built with OpenAI/Gemini to understand student queries.
* **Live DB Interaction**: The AI generates and executes SQL queries in real-time.
* **Microservices Architecture**: Fully containerized using Docker.

---

## 🛠 Tech Stack

The project follows a modern **Client-Server** architecture:

* **Frontend**: [Next.js](https://nextjs.org/) / React - A responsive chat interface.
* **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python) - High-performance server-side logic.
* **Database**: [PostgreSQL](https://www.postgresql.org/) - Managed via [SQLModel](https://sqlmodel.tiangolo.com/) (ORM).
* **AI Engine**: OpenAI GPT-4 / Google Gemini 1.5 Pro.
* **Infrastructure**: [Docker](https://www.docker.com/) & Docker Compose for orchestration.

---

## ⚙️ Installation & Running Locally

### ⚠️ Prerequisites - Security Note
For security reasons, this repository **does not contain**:
1.  **API Keys**: You must provide your own OpenAI or Gemini keys.
2.  **AI Prompts**: The system prompts and DB Schemas are stored in a local `.env` file and are not part of the source code.

### Steps to Run:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/smart-campus-assistant.git](https://github.com/your-username/smart-campus-assistant.git)
    cd smart-campus-assistant
    ```

2.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add your credentials:
    ```env
    # AI Config
    OPENAI_API_KEY=your_key_here
    GEMINI_API_KEY=your_key_here
    
    # Database Config
    DATABASE_URL=postgresql://postgres:postgres@db:5432/smart_campus
    
    # AI System Prompts (Crucial for the Agent to work)
    SYSTEM_PROMPT="You are the official Smart Campus Assistant..."
    DB_SCHEMA="Table Student: id, full_name; Table Course: id, name, code; ..."
    ```

3.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

4.  **Access the application:**
    * **Frontend**: `http://localhost:3000`
    * **Backend API**: `http://localhost:8080`

---

## 🏗 Architecture Detail

The system is designed with a **Retrieval-Augmented Generation (RAG)** approach:
1.  The user sends a message via the **Next.js** frontend.
2.  The **FastAPI** backend injects the **DB Schema** and **System Prompt** from the `.env` file.
3.  The **AI Provider** analyzes the request and generates a specific SQL query.
4.  The backend executes the query on the **PostgreSQL** instance and returns the data to the AI.
5.  The AI formulates a natural language response back to the student.

---

## 👨‍💻 Author
**Yarin Shushan**
4th Year Software Engineering Student @ Afeka College
