# Event Management System

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

## Prerequisites
- Docker
- Docker Compose

## Setup Instructions
1. **Clone the Project**:
   ```bash
      git clone https://github.com/Gangadhar454/event_management_system.git   
      cd event_management_system
   ```
2. **Build and Run with Docker**:
   - Run: `docker compose up --build`
   - The `event_manager` container uses `wait-for.sh` to wait until the PostgreSQL `db` container is live (checked via `pg_isready`) before running migrations and starting Gunicorn.
   - Access the API at `http://localhost:8000` and Swagger at `http://localhost:8000/swagger/`.

3. **Run Tests**:
   - Find the `event_manager` container ID: `docker ps`
   - Run: `docker exec -it <container_id> python manage.py test`

4. **Stop Containers**:
   - Run: `docker-compose down`

## API Endpoints
All endpoints are accessible at `http://localhost:8000`. Use the Swagger UI at `/swagger/` for interactive testing. All `curl` commands assume the API is running locally on June 08, 2025, 04:04 PM IST.

### 1. Create an Event (POST /events)
Creates a new event with specified details.
```bash
curl -X POST http://localhost:8000/events/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Gangadhar Tech conference",
    "location": "Hyderabad Convention Center",
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
curl -X GET http://localhost:8000/events/{event_id}/attendees/?page=1
```
