
function run
{
    docker-compose stop
    docker-compose up -d  --no-recreate
}

function init
{
    docker-compose stop
    docker-compose down -v
    docker volume create pgdata 
    docker-compose up -d  --build

    docker exec -it backend python /usr/src/tradelytics/manage.py recreate_db
}

function stop
{
    docker-compose stop
}

function log
{
    docker-compose logs
}

function test
{
    docker-compose exec backend python -m pytest "app/tests" -p no:warnings
}


# Commands information
function default
{
    echo
    echo "Usage: ./docker.sh <COMMAND>"
    echo
}


case "$1" in
    "test" | "t" )
        test
    ;;
    "run" | "r" )
        run
    ;;
    "log" | "l" )
        log
    ;;
    "stop" | "s" )
        stop
    ;;
    "init" | "init" )
        init
    ;;
    * )
        default
    ;;
esac
