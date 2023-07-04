## Docker command

### build
```shell
docker-compose build --no-cache
```
### initialize ( **don't use unless the project is restructured** )
```shell
docker-compose run --entrypoint "poetry init \
                   --name millionaire --dependency fastapi \
                   --dependency uvicorn[standard]" millionaire
```


### run
```shell
docker-compose run --entrypoint "poetry install" millionaire  
```

### up
```shell
docker-compose up
```
### down
```shell
docker-compose down
```