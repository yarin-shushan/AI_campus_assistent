# 🎓 Smart Campus Assistant - Afeka College

An intelligent full-stack system designed to assist students at Afeka College. The system features an AI-powered agent capable of understanding natural language and interacting directly with campus databases to provide real-time information about courses, classrooms, and student data.

---

## 🛠 Tech Stack & Architecture

The project follows a modern **Client-Server** architecture, fully containerized:

* **Frontend**: [Next.js](https://nextjs.org/) / React - Responsive chat interface.
* **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python) - High-performance server-side logic.
* **Database**: [PostgreSQL](https://www.postgresql.org/) - Managed via [SQLModel](https://sqlmodel.tiangolo.com/).
* **AI Engine**: OpenAI GPT-4 / Google Gemini 1.5 Pro.
* **Infrastructure**: [Docker](https://www.docker.com/) & Docker Compose.

---

## 🔐 Security Framework

Security was a top priority in this project, implemented across several layers:

1.  **Authentication & Authorization**:
    * **JWT (JSON Web Tokens)**: Secure user sessions and identity verification.
    * **Password Hashing**: Using `passlib` with `bcrypt` to ensure no plain-text passwords are stored.
2.  **Infrastructure Security (AWS)**:
    * **Security Groups**: The RDS database is protected by specific AWS firewall rules, allowing access only to specific IP addresses (Whitelisting).
    * **Environment Isolation**: Sensitive data such as **API Keys** and **System Prompts** are never hardcoded. They are managed via `.env` files which are excluded from version control (`.gitignore`).
3.  **Database Protection**:
    * The AI agent is restricted to **Read-Only** queries where applicable to prevent accidental data manipulation.

---

## 🚀 Deployment

The system is designed for a hybrid-cloud deployment:

* **Frontend**: Deployed on **Vercel** for optimal global delivery and Edge functions support.
* **Backend**: Containerized with **Docker** and deployed on **AWS App Runner**, providing a scalable, managed environment for the FastAPI server.
* **Database**: Managed **AWS RDS (PostgreSQL)** instance, ensuring high availability and automated backups.
* **CI/CD**: Seamless integration between GitHub and the deployment platforms for automated builds.

---

## ⚙️ Installation & Running Locally

### ⚠️ Security Note
This repository **does not contain** API Keys or AI Prompts. You must provide your own in a local `.env` file.

1.  **Clone & Navigate**:
    ```bash
    git clone [https://github.com/your-username/smart-campus-assistant.git](https://github.com/your-username/smart-campus-assistant.git)
    cd smart-campus-assistant
    ```

2.  **Environment Setup**:
    Create a `.env` file in the root:
    ```env
    # AI Credentials
    OPENAI_API_KEY=your_key_here
    GEMINI_API_KEY=your_key_here
    
    # DB URL (Local or Remote)
    DATABASE_URL=postgresql://postgres:postgres@db:5432/smart_campus
    
    # System Instructions (Hidden from Git)
    SYSTEM_PROMPT="You are the official Smart Campus Assistant..."
    DB_SCHEMA="Table Student: id, full_name; Table Course: id, name, code; ..."
    ```

3.  **Launch**:
    ```bash
    docker-compose up --build
    ```

---

## 🏗 Workflow
1. User asks a question → 2. Backend injects Schema & Prompt → 3. AI generates SQL → 4. Query executes on RDS → 5. AI returns natural language response.

---

## 👨‍💻 Author
**Yarin Shushan**
4th Year Software Engineering Student @ Afeka College
