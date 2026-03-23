---
name: deploy
description: Deploy the application to production. Runs tests, builds, and pushes.
disable-model-invocation: true
---

# Deploy to Production

Deploy the application to the `$ARGUMENTS` environment (default: staging).

## Steps

1. **Run the test suite** — abort if any test fails
   ```bash
   pytest --tb=short -q
   ```

2. **Check for uncommitted changes** — abort if the working tree is dirty
   ```bash
   git status --porcelain
   ```

3. **Build the Docker image**
   ```bash
   docker build -t hfa-analytics:latest .
   ```

4. **Push to container registry**
   ```bash
   docker tag hfa-analytics:latest ecr.us-west-2.amazonaws.com/hfa-analytics:latest
   docker push ecr.us-west-2.amazonaws.com/hfa-analytics:latest
   ```

5. **Deploy to ECS**
   ```bash
   aws ecs update-service --cluster hfa-prod --service analytics --force-new-deployment
   ```

6. **Verify** — wait 60 seconds, then check the health endpoint
   ```bash
   curl -f https://api.hfa-analytics.com/api/v1/health
   ```

## Important
- Never deploy directly to production without passing through staging first
- If any step fails, stop immediately and report the error
- After deploy, monitor the Grafana dashboard for 5 minutes
