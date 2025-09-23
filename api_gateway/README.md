docker-compose up -d    
docker logs kong-deck   
docker exec -it kong-deck deck sync --kong-addr http://kong:8001 -s /kong.yml    
docker-compose run --rm kong-deck             
