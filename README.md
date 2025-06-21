# CountCRMSystem

Ein internes CRM-System zur Verwaltung von FPV-Drohnenflüssen und Lagerbeständen.

## 🧠 Projektübersicht

CountCRMSystem ist ein selbst entwickeltes Backoffice-System, das den Lebenszyklus von Drohnen (Eingang, Ausgabe, Position und Status) verfolgt. Es wurde mit Fokus auf Clean Architecture, Kapselung der Logik und verständliche Strukturierung entwickelt – vollständig ohne Team, rein aus Eigeninitiative.

---

## ⚙️ Tech-Stack

**Backend:**
- Django
- Django Rest Framework (DRF)
- PostgreSQL
- (Optional: Celery + Redis für Background Tasks)

**Frontend:**
- HTML + Bootstrap
- JavaScript
- Jinja2 Templates
- Chart.js für Visualisierungen

**Deployment & Tools:**
- Git + GitHub
- Pycharm
- Authentifizierung via Django Auth System

---

## 🔧 Features

- ✅ Login mit Django-Auth
- ✅ CRUD für Drohnenflüsse
- ✅ Sortierung nach Datum (auf/ab)
- ✅ Logik getrennt in eigene Klassen
- ✅ Übersichtliche Templatestruktur
- ✅ Einsatz von OOP-Prinzipien (z. B. Kapselung, Liskov-Prinzip)
- ✅ Klare Trennung von Views, Logik und Präsentation
- 🕹️ Erweiterbar um API-only Betrieb, Celery oder Admin-Dashboard

---

## 🚀 Installation

```bash
git clone https://github.com/leprekon122/CountCRMSystem.git
cd CountCRMSystem
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

python manage.py createsuperuser
