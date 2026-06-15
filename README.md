# 📈 Trade Order Management System

> A production-grade **AI-powered Trade Order Management System** built with **FastAPI**, **PostgreSQL**, and **Google Gemini AI**. This backend system simulates a real-world stock trading platform where users can register, login, buy/sell stocks, manage their portfolio, and get AI-powered investment advice.

---

## 🌟 Project Overview

This project was built to demonstrate a complete backend system similar to what is used in real fintech companies like **Zerodha**, **Groww**, and **JP Morgan**. It includes everything from database design to JWT authentication to AI integration.

The system handles the complete lifecycle of a trade:
- A user registers and logs in securely
- They browse available stocks
- They place buy or sell orders
- Their portfolio updates automatically
- Every transaction is logged
- They can ask AI for investment advice

---

## 🚀 Live Demo

> API Documentation: [Swagger UI](https://your-deployment-url.onrender.com/docs)

---

## 🧠 AI Features

### Stock Advice Chatbot
Users can ask any stock market question and receive AI-generated advice powered by Google Gemini 2.5 Flash. Example questions:
- "Should I buy AAPL stock today?"
- "What is the best sector to invest in right now?"
- "How do I diversify my portfolio?"

### Portfolio Analysis
The AI analyzes the user's current holdings and provides:
- Diversification advice
- Risk level assessment
- Suggestions for improvement

---

## 🛠️ Tech Stack

| Category | Technology | Why Used |
|---|---|---|
| **Language** | Python 3.11 | Easy, powerful, widely used in fintech |
| **Framework** | FastAPI | Fast, modern, auto-generates Swagger docs |
| **Database** | PostgreSQL | Industry standard relational database |
| **ORM** | SQLAlchemy | Write Python instead of raw SQL |
| **Authentication** | JWT Tokens | Stateless, secure, industry standard |
| **Password Security** | Bcrypt + Passlib | One-way hashing, cannot be reversed |
| **AI** | Google Gemini 2.5 Flash | Fast, free tier, powerful AI model |
| **API Docs** | Swagger UI | Auto-generated, interactive documentation |
| **Version Control** | Git + GitHub | Industry standard code management |

---

## ✨ Features

### 🔐 Authentication System
- **User Registration** – New users can sign up with username, email, and password
- **Password Hashing** – Passwords are hashed using bcrypt before storing. Even if the database is hacked, passwords cannot be recovered
- **JWT Login** – After login, users receive a JWT token that expires in 24 hours
- **Token Verification** – Every protected route verifies the JWT token before allowing access
- **Role Based Access** – System supports two roles: `user` and `admin`. Admin has extra privileges

### 📊 Stock Management
- **Add Stock** – Admin can add new stocks with symbol, name, and price
- **View Stocks** – All logged-in users can view available stocks
- **Update Stock** – Admin can update stock prices
- **Delete Stock** – Admin can remove stocks from the system

### 💹 Trading System
- **Buy Stock** – Users can buy any available stock by specifying symbol, quantity, and price
- **Sell Stock** – Users can sell stocks they own. System validates they have enough shares before allowing the sale
- **Auto Portfolio Update** – When a user buys stock, portfolio is automatically updated. When they sell, portfolio quantity is reduced
- **Auto Transaction Log** – Every buy or sell automatically creates a transaction record for audit purposes

### 📁 Portfolio Management
- **View Holdings** – Users can see all stocks they currently own
- **Quantity Tracking** – System tracks exact number of shares owned
- **Average Price** – System tracks the average price at which shares were bought

### 📋 Order History
- **Complete History** – Users can view all their past buy and sell orders
- **Order Status** – Each order shows its execution status
- **Timestamps** – Every order is timestamped for record keeping

### 👑 Admin Panel
- **View All Users** – Admin can see all registered users
- **View All Orders** – Admin can see all orders placed by all users
- **View All Transactions** – Admin can see complete transaction history

### 🤖 AI Assistant
- **Stock Advice** – Real-time AI advice on any stock market question
- **Portfolio Analysis** – AI analyzes user's portfolio and gives personalized advice
- **Powered by Gemini** – Uses Google's latest Gemini 2.5 Flash model

---

## 📁 Project Structure

```
trade_order_system/
├── app/
│   ├── dependencies/
│   │   └── auth.py              # JWT token verification + get current user
│   ├── models/
│   │   ├── user.py              # Users table definition
│   │   ├── stock.py             # Stocks table definition
│   │   ├── orders.py            # Orders table definition
│   │   ├── portfoliotable.py    # Portfolio table definition
│   │   └── transaction.py       # Transactions table definition
│   ├── routers/
│   │   ├── auth.py              # POST /signup, POST /login
│   │   ├── user.py              # GET /profile, /orders, /portfolio
│   │   ├── stocks.py            # CRUD operations for stocks
│   │   ├── orders.py            # POST /buy, POST /sell, GET /orders
│   │   ├── admin.py             # Admin only routes
│   │   └── ai.py                # AI advice and portfolio analysis
│   ├── schemas/
│   │   ├── user.py              # UserCreate, UserResponse schemas
│   │   ├── stock.py             # StockCreate, StockResponse schemas
│   │   ├── orders.py            # OrderCreate, OrderResponse schemas
│   │   ├── portfoliotable.py    # PortfolioResponse schema
│   │   └── transaction.py       # TransactionResponse schema
│   ├── utils/
│   │   ├── jwt.py               # create_token, verify_token functions
│   │   └── security.py          # hash_password, verify_password functions
│   ├── database.py              # SQLAlchemy engine, session, base setup
│   ├── exceptions.py            # Global exception handlers
│   └── main.py                  # FastAPI app, router registration, table creation
├── .env                         # Environment variables (not in GitHub)
├── .gitignore                   # Files to ignore in git
└── README.md                    # Project documentation
```

---

## 🗄️ Database Design

### Entity Relationship

```
Users ──────┬──── Orders
            ├──── Portfolio
            └──── Transactions

Stocks ─────┬──── Orders (via stock_symbol)
            ├──── Portfolio (via stock_symbol)
            └──── Transactions (via stock_symbol)
```

### Users Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | Integer | Primary Key, Auto Increment | Unique user identifier |
| username | String | Unique, Indexed | User's display name |
| email | String | Unique, Indexed | User's email address |
| password | String | Not Null | Bcrypt hashed password |
| role | String | Default: "user" | user or admin |

### Stocks Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique stock identifier |
| symbol | String | Unique, Indexed | Stock ticker (AAPL, TSLA) |
| name | String | Not Null | Company full name |
| price | Float | Not Null | Current stock price |

### Orders Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique order identifier |
| user_id | Integer | Foreign Key → Users | Who placed the order |
| stock_symbol | String | Not Null | Which stock was traded |
| order_type | String | Not Null | BUY or SELL |
| quantity | Integer | Not Null | Number of shares |
| price | Float | Not Null | Price per share at time of order |
| status | String | Default: EXECUTED | Order execution status |
| created_at | DateTime | Auto | When order was placed |

### Portfolio Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique portfolio entry |
| user_id | Integer | Foreign Key → Users | Portfolio owner |
| stock_symbol | String | Not Null | Which stock is held |
| quantity | Integer | Not Null | Number of shares currently owned |
| avg_price | Float | Not Null | Average price paid per share |

### Transactions Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique transaction identifier |
| user_id | Integer | Foreign Key → Users | Who made the transaction |
| stock_symbol | String | Not Null | Which stock was transacted |
| transaction_type | String | Not Null | BUY or SELL |
| quantity | Integer | Not Null | Number of shares |
| price | Float | Not Null | Price per share |
| created_at | DateTime | Auto | When transaction occurred |

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | /signup | Register new user account | ❌ Public |
| POST | /login | Login and receive JWT token | ❌ Public |

### User Routes
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | /user/profile | Get logged in user profile | ✅ User |
| GET | /user/orders | Get all orders of logged in user | ✅ User |
| GET | /user/portfolio | Get portfolio of logged in user | ✅ User |

### Stock Routes
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | /stocks/ | Get list of all stocks | ✅ User |
| POST | /stocks/ | Add new stock to system | 👑 Admin |
| PUT | /stocks/{symbol} | Update stock price | 👑 Admin |
| DELETE | /stocks/{symbol} | Remove stock from system | 👑 Admin |

### Order Routes
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | /orders/ | Place new buy or sell order | ✅ User |
| GET | /orders/ | Get all orders | ✅ User |

### Admin Routes
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | /admin/users | View all registered users | 👑 Admin |
| GET | /admin/orders | View all orders in system | 👑 Admin |
| GET | /admin/transactions | View all transactions | 👑 Admin |

### AI Routes
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | /ai/advice | Get AI stock market advice | ✅ User |
| POST | /ai/analyze-portfolio | Get AI portfolio analysis | ✅ User |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- PostgreSQL installed and running
- Git installed
- Google Gemini API key (free at aistudio.google.com)

### Step 1 — Clone the repository
```bash
git clone https://github.com/Dev2414/trade_order_system.git
cd trade_order_system
```

### Step 2 — Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install all dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv passlib bcrypt python-jose requests
```

### Step 4 — Create PostgreSQL database
```sql
CREATE DATABASE trade_system;
```

### Step 5 — Setup environment variables
Create a `.env` file in the root directory:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/trade_system
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 6 — Run the application
```bash
uvicorn app.main:app --reload
```

### Step 7 — Access API documentation
Open your browser and go to:
```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

```
SIGNUP:
User sends {username, email, password}
      ↓
Pydantic validates all fields
      ↓
Check if email already exists
      ↓
Hash password using bcrypt
      ↓
Save user to PostgreSQL
      ↓
Return user data (without password)

LOGIN:
User sends {email, password}
      ↓
Find user by email in database
      ↓
Verify password against hash
      ↓
Generate JWT token (expires in 24 hours)
      ↓
Return JWT token to user

PROTECTED ROUTES:
User sends request with token in header
Authorization: Bearer eyJhbGci...
      ↓
System extracts token
      ↓
Verify token signature and expiry
      ↓
Extract email from token payload
      ↓
Find user in database
      ↓
Allow or deny access
```

---

## 💹 Trading Flow

```
BUY ORDER:
User sends {stock_symbol, order_type: "BUY", quantity, price}
      ↓
Verify JWT token → get current user
      ↓
Check if stock exists in database
      ↓
Create order record (status: EXECUTED)
      ↓
Check if user already owns this stock
  → YES: Add quantity to existing portfolio entry
  → NO: Create new portfolio entry
      ↓
Create transaction log
      ↓
Save all changes to database
      ↓
Return order details

SELL ORDER:
User sends {stock_symbol, order_type: "SELL", quantity, price}
      ↓
Verify JWT token → get current user
      ↓
Check if stock exists in database
      ↓
Check if user owns this stock
      ↓
Check if user has enough shares to sell
      ↓
Create order record (status: EXECUTED)
      ↓
Reduce quantity in portfolio
  → If quantity becomes 0: Delete portfolio entry
      ↓
Create transaction log
      ↓
Save all changes to database
      ↓
Return order details
```

---

## 🤖 AI Integration Flow

```
User sends question to POST /ai/advice
      ↓
System creates a detailed prompt:
"You are a stock market assistant.
User: {username}
Question: {user_question}"
      ↓
Send prompt to Google Gemini 2.5 Flash API
      ↓
Receive AI generated response
      ↓
Return advice with disclaimer
```

---

## 🔑 Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | postgresql://postgres:password@localhost:5432/trade_system |
| `GEMINI_API_KEY` | Google Gemini API key | AQ.xxxxxxxxxxxxx |

---

## 🛡️ Security Features

- **Password Hashing** – All passwords are hashed using bcrypt. Plaintext passwords are never stored
- **JWT Authentication** – Stateless authentication using signed tokens
- **Token Expiry** – JWT tokens expire after 24 hours for security
- **Role Based Access** – Admin and user roles with different permissions
- **Protected Routes** – All sensitive routes require valid JWT token
- **Input Validation** – Pydantic schemas validate all incoming data
- **SQL Injection Prevention** – SQLAlchemy ORM prevents SQL injection attacks

---

## 📊 Business Rules

1. **Email must be unique** – Two users cannot register with the same email
2. **Stock must exist** – Users cannot buy or sell stocks that don't exist in the system
3. **Quantity must be positive** – Order quantity must be greater than zero
4. **Ownership validation** – Users cannot sell stocks they don't own
5. **Sufficient quantity** – Users cannot sell more shares than they own
6. **Every trade is logged** – All buy and sell operations create a transaction record
7. **Portfolio auto-updates** – Portfolio is automatically updated after every trade
8. **Admin only operations** – Only admins can add, update, or delete stocks

---

## 🧪 Testing the API

### Using Swagger UI
1. Open `http://127.0.0.1:8000/docs`
2. Click **POST /signup** → Register a new user
3. Click **POST /login** → Login and copy the access token
4. Click **Authorize** button → Paste the token
5. Now test all protected endpoints

### Test Sequence
```
1. POST /signup          → Create account
2. POST /login           → Get JWT token
3. POST /stocks/         → Add stock (admin only)
4. GET  /stocks/         → View all stocks
5. POST /orders/         → Buy a stock
6. GET  /user/portfolio  → Check portfolio
7. POST /orders/         → Sell a stock
8. GET  /user/orders     → Check order history
9. POST /ai/advice       → Get AI advice
10. POST /ai/analyze-portfolio → Get portfolio analysis
```

---

## 👨‍💻 Author

**Divanshu Gangadhari**
- GitHub: [@Dev2414](https://github.com/Dev2414)
- Email: divanshugangadhari@gmail.com
- LinkedIn: [Your LinkedIn URL]

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Google Gemini AI](https://ai.google.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Passlib Documentation](https://passlib.readthedocs.io/)

---

⭐ If you found this project helpful, please give it a star on GitHub!
