#!/bin/bash

# Step 1: Enter the Redis container and delete all Celery task-related keys
echo "Deleting all Celery task-related keys from Redis..."

docker exec -it celery-demo-redis-1 redis-cli EVAL "for _,k in ipairs(redis.call('keys', ARGV[1])) do redis.call('del', k) end" 0 "celery-task-meta-*"

# Optionally, delete other Celery-related keys as needed
# docker exec -it celery-demo-redis-1 redis-cli EVAL "for _,k in ipairs(redis.call('keys', ARGV[1])) do redis.call('del', k) end" 0 "unacked-*"
# docker exec -it celery-demo-redis-1 redis-cli EVAL "for _,k in ipairs(redis.call('keys', ARGV[1])) do redis.call('del', k) end" 0 "reserved-*"
# docker exec -it celery-demo-redis-1 redis-cli EVAL "for _,k in ipairs(redis.call('keys', ARGV[1])) do redis.call('del', k) end" 0 "celeryev.*"

echo "All Celery task-related keys deleted."

# Step 2: Restart the Flower service
echo "Restarting the Flower service..."
docker-compose restart flower

echo "Flower service restarted."

# Final message
echo "Redis cleanup and Flower restart completed successfully."
