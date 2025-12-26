# APLUS PUBLICATIONS
## Modern Academic Publication Platform

A professional, high-performance Django ecosystem engineered for **Aplus Publications**. Built with a strictly academic focus, this platform delivers curriculum-aligned resources through a modern, mobile-first experience.

---

### 🌟 Key Features

*   **Modern Academic Catalogue**: HTMX-powered instant search and filtering for Textbooks, Workbooks, and **Past Questions**.
*   **"Cute & Compact" UX**: Premium, high-density visual design optimised for both clarity and aesthetic appeal.
*   **Universal Access (Low-Data Mode)**: Specialised bandwidth-saving mode for students in diverse network environments.
*   **Institutional Support**: Automated Bulk Quote Request system for schools and large organisations.
*   **GES Resource Hub**: Centralised repository for official GES Curricula, Academic Calendars, and Timetables with download tracking.
*   **Unified Academic Hubs**: Custom dashboards for Students, Teachers, and School Administrators to manage acquisitions and resources.
*   **Integrated Payments**: Seamless Paystack Ghana integration for secure, automated transactions.
*   **Academic Enquiry System**: Formal communication channel for institutional inquiries managed via the Admin Portal.

---

### 🛠 Tech Stack & Standards

*   **Framework**: Django 4.2+ (Python 3.13)
*   **Frontend**: Tailwind CSS + HTMX (Single Page Application feel)
*   **Localization**: British English (`en-gb`) & GMT Standards
*   **Performance**: WhiteNoise with Brotli compression, Database connection pooling
*   **Database**: PostgreSQL ready (via dj-database-url)
*   **Security**: Content Security Policy (CSP), UUID-protected transaction links, Environment-based hardening

---

### 🎨 Brand Identity

*   **Primary**: Lemon Green (#C3D600)
*   **Secondary**: Golden Brown (#96691D)
*   **Typography**: Inter (Modern sans-serif)
*   **Style**: Strictly Academic, Professional, Minimalist

---

### 🚀 Production Deployment

1. **Environment Config**: Populate `.env` from `.env.example`.
2. **Payment Setup**: Configure `PAYSTACK_SECRET_KEY` and `PAYSTACK_PUBLIC_KEY`.
3. **Cloud Storage**: Set `GS_BUCKET_NAME` for hosting Academic PDFs and high-res covers.
4. **Hardening**: Set `DEBUG=False` to trigger automated SSL, HSTS, and Secure Cookie protocols.

---

### 🛠 Development Commands

```bash
# Initialise Environment
pip install -r requirements.txt

# Database Synchronisation
python manage.py makemigrations
python manage.py migrate

# Access Control
python manage.py createsuperuser

# Execution
python manage.py runserver
```

---

**Engineered by Insight Innovations**  
*Strictly Academic. Scalable. Secure.*
