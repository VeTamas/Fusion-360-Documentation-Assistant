# Docker Deploy Skill

Use this skill when asked to rebuild, restart, or deploy the application.

## Steps

1. Stop running containers:
   docker compose down

2. Rebuild the app image:
   docker compose build app

3. Start all services:
   docker compose up -d

4. Run database migrations:
   docker exec rag_app alembic upgrade head

5. Verify health:
   docker compose ps
   docker logs rag_app --tail 20

## Notes
- Always run migrations after rebuild
- PostgreSQL must be healthy before app starts (healthcheck in compose)
- If vectorstore is empty, run: python app/rag/embeddings.py
