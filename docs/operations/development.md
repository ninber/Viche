# Development

## Local Stack

Start the local skeleton:

```bash
docker compose up --build
```

Services:

- Web: `http://localhost:3000`
- API: `http://localhost:8000/v1/health`
- API docs: `http://localhost:8000/docs`
- Keycloak: `http://localhost:8080`
- MinIO console: `http://localhost:9001`

Default local credentials are development-only and must not be used in production.

