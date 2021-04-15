
# Deploying w. Docker & Gitlab CI

```yaml
deploy:
  stage: deploy
  script:
    - echo "deploying to $ENV"
    - if [ "$ENV" == "staging" ]; then REMOTE=$STAGING_USER@$STAGING_HOST; else REMOTE=$PROD_USER@$PROD_HOST; fi
    - export REMOTE=${REMOTE}
    - envsubst < docker-compose.yml > docker-compose.$ENV.yml
    - scp ./env.list ./docker-compose.$ENV.yml "$REMOTE:"
    - ssh $REMOTE docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - ssh $REMOTE docker pull $IMAGE_NAME
    - ssh $REMOTE docker pull $IMAGE_NAME_NGINX
    - ssh $REMOTE docker-compose --env-file .env -f docker-compose.$ENV.yml up -d
  rules:
    - if: $CI_COMMIT_BRANCH == 'master' || $CI_COMMIT_BRANCH == 'dev'
```
