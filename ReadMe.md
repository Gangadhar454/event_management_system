# Mini Event Management System API

A Django-based REST API for managing events and attendees, with PostgreSQL, timezone support using **pendulum**, Swagger documentation via **drf-yasg**, and class-based views. The application is containerized with Docker and Docker Compose, ensuring portability and scalability.

## Features
- **Event Management**: Create and list upcoming events with name, location, start/end times, max capacity, and timezone.
- **Attendee Registration**: Register attendees for events, preventing overbooking and duplicate registrations.
- **Attendee Export**: Export event attendees to Excel for reporting.
- **Timezone Handling**: Stores times in UTC, displays in the specified timezone (default: Asia/Kolkata).
- **Pagination**: Lists attendees with pagination (default page size: 10).
- **Data Integrity**: Enforces constraints like unique attendee emails per event and max capacity limits.
- **Swagger Documentation**: Interactive API docs at `/swagger/`.
- **Unit Tests**: Covers all endpoints and edge cases.
- **Dockerized Setup**: Runs Django with Gunicorn and PostgreSQL, with `wait-for.sh` ensuring the `event_manager` container waits for the `db` container to be live.

## Project Structure
event_management_system/
├── Dockerfile
├── docker-compose.yml
├── wait-for.sh
├── README.md
├── manage.py
├── event_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── apps.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── event.py
│   │   ├── attendee.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── event_service.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── event_views.py
│   │   ├── attendee_views.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── event_serializer.py
│   │   ├── attendee_serializer.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_event_api.py
│   │   ├── test_attendee_api.py
├── requirements.txt


## Prerequisites
- Docker and Docker Compose installed.
- Basic understanding of Django, REST APIs, and `curl`.

## Setup Instructions
1. **Clone or Unzip the Project**:
   - Unzip the project: `unzip event_management_system_django_docker.zip`
   - Navigate to the directory: `cd event_management_system`

2. **Ensure `wait-for.sh` is Executable**:
   - Run: `chmod +x wait-for.sh` (Linux/Mac)

3. **Build and Run with Docker**:
   - Run: `docker-compose up --build`
   - The `event_manager` container uses `wait-for.sh` to wait until the PostgreSQL `db` container is live (checked via `pg_isready`) before running migrations and starting Gunicorn.
   - Access the API at `http://localhost:8000` and Swagger at `http://localhost:8000/swagger/`.

4. **Run Tests**:
   - Find the `event_manager` container ID: `docker ps`
   - Run: `docker exec -it <container_id> python manage.py test`

5. **Stop Containers**:
   - Run: `docker-compose down`

## API Endpoints
All endpoints are accessible at `http://localhost:8000`. Use the Swagger UI at `/swagger/` for interactive testing. All `curl` commands assume the API is running locally on June 08, 2025, 04:04 PM IST.

### 1. Create an Event (POST /events)
Creates a new event with specified details.
```bash
curl -X POST http://localhost:8000/events/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Tech Conference 2025",
    "location": "Bangalore Convention Center",
    "start_time": "2025-06-10T09:00:00+05:30",
    "end_time": "2025-06-10T17:00:00+05:30",
    "max_capacity": 100,
    "timezone": "Asia/Kolkata"
}'
```
### 2. List Upcoming Events (GET /events)
```bash
curl -X GET http://localhost:8000/events/
```

### 3. Register Attendee (POST /events/{event_id}/register)
```bash
curl -X POST http://localhost:8000/events/{event_id}/register/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Gangadhar",
    "email": "gangadhar@gmail.com"
}'
```

### 4. List attendees of an event
```bash
curl -X GET http://localhost:8000/events/1/attendees/?page=1
```
