# Saju Cafe: Saju-Based Personality Analysis Web Service

> A Flask-based web application that analyzes a user's personality based on their "Saju" (the Four Pillars of Destiny, derived from birth date and time) and matches it to a modern MBTI type to generate a unique "Fortune Card."


## 🚀 Key Features

* **User Authentication:** Secure user registration, login, and session management using `Flask-Login`.
* **Saju Data Analysis:** Utilizes the `sajupy` library combined with custom logic to translate a user's `birth_datetime` into the 8 Saju characters (Ganji) and Ohaeng (Five Elements) data.
* **Personality & MBTI Matching Engine:**
    * **Day Master (日干) Analysis:** Determines the user's core personality from one of the 10 "Day Masters" (e.g., 甲, 乙, 丙...).
    * **Five Elements Scoring:** Analyzes the 8 characters to calculate the distribution score of Wood (木), Fire (火), Earth (土), Metal (金), and Water (水).
    * **MBTI Inference:** A **custom-built rules engine** that infers the most likely MBTI type by mapping the Yin/Yang of the Day Master (E/I) and the strength of the Five Elements scores (S/N, T/F, J/P).
* **Dynamic Card Generation:**
    * Generates a unique result card by combining the inferred MBTI, personality description, a random color, and a matched celebrity (name + image).
    * Ensures stable image serving by referencing image resources stored locally in the `static` folder.
* **Asynchronous API:**
    * After rendering the initial page skeleton with Jinja, the application uses a JavaScript `fetch` call to an asynchronous API endpoint (`POST /api/generate_card`).
    * This provides a dynamic UX, playing card-drawing sounds and animations *before* updating the screen with the final results.
* **Saju Detail Modal:** On-click modal window that displays detailed Saju information (the 8 pillars, Ohaeng distribution) without requiring a page reload.

---

## 🏗️ System Architecture

This project follows an **MVT (Model-View-Template)** architecture based on the Flask framework. The user request flow is as follows:

1.  **Client (Browser - `card.html`)**: User clicks the "Draw Card" button.
2.  **JavaScript (`card_generate.js`)**: A `fetch` call is made to the server's API endpoint.
3.  **Web Server (Flask - `routes/main.py`)**: The `@main_bp.route('/api/generate_card')` endpoint receives the request.
4.  **Business Logic (`saju_logic/calculator.py`)**:
    * The `analyze_saju()` function is executed using the `current_user.birth_datetime`.
    * Calls the `sajupy` library and runs the custom Five Elements scoring logic.
    * Executes the MBTI matching rules engine.
    * Assembles the final data (celebrity, random color, etc.).
5.  **Data (Flask-SQLAlchemy)**: User information (`birth_datetime`) is retrieved from the `current_user` object.
6.  **Response**: The analysis results are returned to the client as `JSON`.
7.  **Client (Browser - `card_generate.js`)**: The `data` is received, and the JavaScript updates the HTML DOM elements (`<img>`, `<span>`, etc.) in real-time to display the result card.

---

## 🛠️ Tech Stack

### Backend
* **Python 3.12**
* **Flask**: Micro web framework
* **Flask-SQLAlchemy**: ORM and database management
* **Flask-Login**: User session and authentication management
* **sajupy**: A library for Saju (Korean astrology) calculations

### Frontend
* **HTML5**
* **CSS3**: Card styling and modal animations
* **JavaScript (ES6+)**:
    * DOM manipulation
    * `fetch` API (Asynchronous communication)
    * Click event and modal control
* **Jinja2**: Flask templating engine

### Database
* **SQLite** (Development) / Compatible with **PostgreSQL** (Production)

---
