<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=90&section=header"/>

# 🤖 GemoraAI — Gemini API Intelligent Chat Bot

GemoraAI is a **full-stack conversational chatbot** built with **Flask**, **React**, and **Google’s Gemini API**.  
It delivers real-time, natural replies in an elegant UI, supports **JWT-secured authentication**, and stores user chat history using **PostgreSQL**.

---

## 🚀 Features

✅ **AI-Powered Replies** — Uses Google Gemini API (Generative AI)  
✅ **JWT Authentication** — Secure login, signup, and token refresh  
✅ **Persistent Chat History** — Every conversation is saved per user  
✅ **Modern UI** — Built with React + TailwindCSS + Framer Motion  
✅ **PostgreSQL Database** — Managed via Flask SQLAlchemy ORM  
✅ **Rate Limiting & Caching** — Prevents spam and boosts performance  
✅ **Error-Proof Architecture** — Flask Blueprints, modular backend  
✅ **Real-Time UX** — AI “thinking” indicator + smooth animations  
✅ **Session Handling** — Auto logout when token expires  

---

## 🧩 Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| **Frontend** | React 18, Vite, Tailwind CSS, Framer Motion, Zustand, Axios | UI, animations, state management |
| **Backend** | Flask, Flask-JWT-Extended, SQLAlchemy, Flask-Limiter, Flask-CORS | API, authentication, rate limiting |
| **AI Engine** | Google Gemini API | Natural language generation |
| **Database** | PostgreSQL | Stores users, chats, messages |
| **Cache (optional)** | Redis | Speeds up frequent AI queries |
| **Deployment** | Render / Railway / Docker | Cloud-ready backend + frontend |

---

## 🗂️ Project Structure
```
Gemora-AI/
│
├── backend/
│ ├── app.py # Main Flask entry point
│ ├── config.py # Config & env variables
│ ├── .env.example # Example env template
│ ├── requirements.txt # Python dependencies
│ │
│ ├── models/ # SQLAlchemy models (User, Message, ChatSession)
│ ├── routes/ # API routes (auth, chat)
│ ├── utils/ # Helpers (DB, JWT, Gemini client, caching)
│ └── migrations/ (optional) # Alembic migrations
│
└── frontend/
├── src/
│ ├── pages/Chat.jsx # Chat interface
│ ├── pages/Login.jsx # Login page
│ ├── pages/Signup.jsx # Signup page
│ ├── api/axios.js # API config (Axios)
│ ├── store/useAuthStore.js
│ └── components/
│
├── public/
├── package.json
└── vite.config.js
```

---

## ⚙️ Installation & Setup

### 🐍 Backend (Flask)

```
cd backend
python -m venv venv
venv\Scripts\activate        # (Windows)
# source venv/bin/activate   # (Linux / macOS)
pip install -r requirements.txt
cp .env.example .env
```

### ⚙️ Create and Configure your .env
```
FLASK_ENV=development
SECRET_KEY=your_flask_secret
JWT_SECRET_KEY=your_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/gemora_db
RATE_LIMITER_STORAGE=memory://
CORS_ORIGINS=http://localhost:5173
```
and put it on backend/ dir

### ✅ Run Flask
```
python app.py
```

### ⚛️ Frontend (React + Vite)
```
cd ../frontend
npm install
npm run dev
```

### ↪️ Open the app in your browser:
```
🌐 http://localhost:5173
```

### 🧠 Environment Variables

| Variable | Description |
|-------|-------------|
| **GEMINI_API_KEY** | Google Generative AI key |
| **JWT_SECRET_KEY** | Token signing secret |
| **GEMINI_API_KEY** | PostgreSQL connection string |
| **DATABASE_URL** | Redis or in-memory limiter |
| **CORS_ORIGINS** | Allowed frontend URLs |

### 🛡️ Security & Best Practices

✅ Passwords hashed with bcrypt
✅ JWT tokens for secure sessions
✅ Input validation & email regex checking
✅ HTTPS & CSP via Flask-Talisman (optional)
✅ Rate limiting with Flask-Limiter
✅ Tokens stored securely in localStorage
✅ Auto logout when JWT expires

### 🧩 API Endpoints
#### 🔐 Authentication

| Method | Endpoint | Description |
|-------|-------------|---------------|
| **POST** | /api/auth/signup | Register new user |
| **POST** | /api/auth/login | Log in and get JWT |
| **POST** | /api/auth/refresh | Refresh access token |
| **GET** | /api/auth/verify | Validate JWT token |

#### 💬 Chat

| Method | Endpoint | Description |
|-------|-------------|---------------|
| **POST** | /api/chat/new | Create new chat + AI first response |
| **POST** | /api/chat/send | Send message & get AI reply |
| **GET** | /api/chat/list | List all chat sessions |
| **GET** | /api/chat/<id>/history | Get full chat history |
| **DELETE** | /api/chat/<id>/delete | Delete chat session |

## 🧠 AI Model

Gemora AI uses Google’s Gemini 2.5 Flash model for response generation.
Fallbacks automatically handle API downtime or invalid responses.

![](https://github.com/idimetrix/BEPb/blob/main/assets/Bottom_down.svg)
>>>>>>> 
