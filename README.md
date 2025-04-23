# Credit card Fraud Detection
By
Bhanu Prakash Akepogu,
Tarun Emmanuel Majhi,
Charan Reddy Devapatla and
Vandana Chinthala

# FastAPI + React + PostgreSQL Dockerized Stack

A full-stack boilerplate that brings together a **FastAPI** backend,
a **React** frontend, and a **PostgreSQL** database—fully containerized 
with Docker Compose for easy development and deployment.

---

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Getting Started](#getting-started)  
  - [Configuration](#configuration)  
  - [Build & Run](#build---run)  
- [Services](#services)  
- [Environment Variables](#environment-variables)  
- [Project Structure](#project-structure)  
- [Accessing the App](#accessing-the-app)  
- [Stopping & Cleaning Up](#stopping---cleaning-up)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- **FastAPI** server with hot reload and built-in OpenAPI docs  
- **React** (Vite) frontend served at port 5173 with live-reload  
- **PostgreSQL** 13 as the primary datastore  
- Single-command setup via Docker Compose  
- Code-volume mounts for instant updates during development  

---

## Prerequisites

- [Docker](https://www.docker.com/) & 
[Docker Compose](https://docs.docker.com/compose/) installed  
- Git (for cloning the repo)  

---

## Getting Started

### Configuration

1. **Clone this repository**  
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```


### Build & Run

From the project root, run:
```bash
docker-compose -f compose.yml up --build
```
This will:

- Build both **backend** and **frontend** images  
- Start containers for `backend`, `frontend`, and `database`  
- Stream logs to your terminal  

---

## Services

| Service    | Image / Build Context                 | Port Mapping      | Description                                 |
|------------|---------------------------------------|-------------------|---------------------------------------------|
| **backend**  | `./backend` (fastapi.dockerfile)       | `8000:8000`        | FastAPI app, reload enabled                 |
| **database** | `postgres:13`                         | `5432:5432`        | PostgreSQL with persistent volume `pgdata`  |
| **frontend** | `./frontend` (frontend.dockerfile)     | `5173:5173`        | React (Vite) dev server                     |

---

## Environment Variables

Load required .env files

## Project Structure

```
.
├── compose.yml
├── frontend/
│   ├── frontend.dockerfile
│   ├── package.json
│   ├── package-lock.json
│   └── src/
└── backend/
    ├── fastapi.dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py        # FastAPI entrypoint
        └── …               # your routers, models, etc.
```

---


## Accessing the App

- **Frontend**: http://localhost:5173  
- **Backend API Docs**: http://localhost:8000/docs  
- **Postgres**: `postgres://postgres:postgres@localhost:5432/postgres`

---

## Stopping & Cleaning Up

To stop:
```bash
docker-compose -f compose.yml down
```

To remove volumes (e.g., reset the database):
```bash
docker-compose -f compose.yml down -v
```

---

## Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feat/your-feature`)  
3. Commit your changes (`git commit -m "Add your feature"`)  
4. Push to your branch (`git push origin feat/your-feature`)  
5. Open a Pull Request  

---

## License

This project is licensed under the [MIT License].

MIT License

Copyright (c) 2025 Bhanu Prakash

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
