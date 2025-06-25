# NexaVote — Electronic Voting System

**NexaVote** is a secure, modular, and scalable electronic voting system built with Django and PostgreSQL, containerized using Docker.

This platform is ideal for managing elections in schools, clubs, organizations, and communities. It supports invite-based voting, user authentication, election creation, candidate management, and secure vote casting.

---

## Project Structure

```bash
.
├── backend/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── .env.sample
│   ├── config/                # Django project
│   ├── users/                 # Custom user model
│   ├── elections/             # Election-related models
│   ├── votes/                 # Vote and ballot logic
│   ├── invitations/           # Invite-based registration
│   ├── static/                # Static files
│   └── templates/             # HTML templates
````

---

## Tech Stack

* **Backend:** Django 5.x
* **Database:** PostgreSQL 15
* **Containerization:** Docker + Docker Compose
* **ORM:** Django Models
* **Authentication:** Custom User Model

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/anuelt2/nexavote.git
cd nexavote/backend
```

### 2. Setup Environment

Create a `.env` file inside `backend/` from .env.sample:

---

### 3. Build & Start the Containers

```bash
docker compose -p nexavote -f docker-compose.yml up --build -d
```

---

### 4. Run Migrations

```bash
docker compose -p nexavote -f docker-compose.yml exec web python manage.py makemigrations
docker compose -p nexavote -f docker-compose.yml exec web python manage.py migrate
```

---

### 5. Create Superuser

```bash
docker compose -p nexavote -f docker-compose.yml exec web python manage.py createsuperuser
```

---

### 6. Access the App

Visit: [http://localhost:8000](http://localhost:8000)

---

## Useful Commands

| Action             | Command                                                               |
| ------------------ | --------------------------------------------------------------------- |
| Build & Run        | `docker compose -p nexavote up --build -d`                            |
| Stop & Clean Up    | `docker compose -p nexavote down -v --remove-orphans`                 |
| View Logs          | `docker compose -p nexavote logs -f`                                  |
| List service names | `docker compose config --services`                                  |
| Run Admin Commands | `docker compose -p nexavote exec web python manage.py <cmd>` |

---

## Work in Progress

The following features are planned or in development:

* [x] User management via invitations
* [ ] Role-based permissions (Admin, Voter)
* [ ] Secure ballot system
* [ ] Election result publishing
* [ ] Email notifications
* [ ] Frontend UI (React or HTMX)

---

## License

MIT License. See [LICENSE](LICENSE) file for more information.

---

## Contributors

* [Emmanuel K. Tettey](https://github.com/anuelt2)
* [Sulem Yong Vasitha F.](https://github.com/vasitha1)

---

```

---

```

