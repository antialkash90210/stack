Стратегия отката:
1. Тег предыдущей стабильной версии известен (хранится в GitLab Container Registry).
2. При неудачном деплое выполнить на целевой ВМ:
   docker pull $CI_REGISTRY_IMAGE:<PREVIOUS_SHA>
   docker tag $CI_REGISTRY_IMAGE:<PREVIOUS_SHA> $CI_REGISTRY_IMAGE:latest
   docker compose up -d
3. Проверить /health.
4. Либо использовать git revert на main и дождаться нового пайплайна.
