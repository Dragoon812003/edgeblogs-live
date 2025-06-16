# 📝 Edge Blogs

**Edge Blogs** is a fully functional blogging platform built using **Django** and **SQLite**.  
It allows users to read, write, and comment on blog posts, while delivering a personalized homepage using a **custom-built recommendation engine** — all done without any machine learning libraries.

---

## 🌐 Live Demo

🔗 [https://edgeblogs.pythonanywhere.com](https://edgeblogs.pythonanywhere.com)

---

## 🚀 Features

### 👥 User Features
- User authentication (signup/login/logout)
- Post blog articles with rich text content
- View, like, and comment on blogs
- Follow authors to get more of their content
- Personalized homepage feed based on blog content and user behavior

---

### 🧠 Recommendation Engine

The platform uses a simple but effective keyword-based system to personalize blog recommendations:

1. **Blog Upload**
   - When a author posts a blog, the content is tokenized.
   - Common English stopwords are removed.
   - The system extracts the **top 10 most frequent keywords**, which define the blog’s **categories** (ranked by importance).

2. **User Interaction Tracking**
   - If a user **reads** a blog, its top keywords are saved to their profile as weak preferences.
   - If a user **likes** a blog, those keywords are weighted more.
   - If a user **follows** an author, that author’s posts are shown higher in their feed.

3. **Ranking Logic**
   - Blogs are ranked for each user based on the **overlap between blog keywords and the user’s interests**.
   - Posts from followed authors are also boosted.

> All logic is built manually using basic Python/Django constructs. No ML/NLP libraries involved.

---

### 💬 Comments
- Users can comment on blog posts.
- Each comment is tied to the blog and the user who posted it.
- Comments are displayed in order with user info.

---

### 📈 View Tracking (via IP Address)
- Each blog's view count is tracked by **visitor IP**.
- Helps prevent view spam and shows actual unique traffic per blog.
- Logged whether the user is signed in or not.

---

## 🧰 Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Tailwind
- **Hosting**: PythonAnywhere
- **No external ML libraries** used

---

## 🎯 Why I Built This

Most content platforms use complex ML or third-party APIs. I wanted to:

* Build my own ranking engine from scratch
* Learn how behavior-based personalization can work without external dependencies
* Create a usable, working platform with deployable logic

---

## 🔮 Future Plans

* Add blog tags and advanced search
* Include support for uploading images inside blog content
* Improve visual design of dashboard & reader pages

---

## 🧑‍💻 Author

**Muhammad Kamkoriwala**
📧 [kamkoriwalamuhammad@gmail.com](mailto:kamkoriwalamuhammad@gmail.com)
🔗 GitHub: [github.com/Dragoon812003](https://github.com/Dragoon812003)

```
