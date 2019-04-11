#!/bin/bash

# created by peter on 2018/5/7


start(){
    cpu_num=`cat /proc/cpuinfo |grep processor|wc -l`
    nohup gunicorn -w $cpu_num -b '127.0.0.1:8081' --log-level debug app:app  >>service.log 2>&1 &
    sleep 3s
    echo "this machine has $cpu_num cpus, so it will boot up $cpu_num workers !"
    worker_num=`ps -ef|grep gunicorn|grep -v grep|wc -l`
    if [ $worker_num == $(($cpu_num+1)) ]
    then
        echo "service start successful !"
    else
        echo "service start failed, please run check: ./run.sh status"
    fi
}

stop(){
    origin_num=`ps -ef|grep gunicorn|grep -v grep|wc -l`
    ps -ef|grep gunicorn|cut -c 9-15|xargs kill -9
    sleep 1s
    current_num=`ps -ef|grep gunicorn|grep -v grep|wc -l`
    if [ $origin_num == 0 ]
    then
        echo "service not running !"
    elif [ $current_num == 0 ]
    then
        echo "service stop successful !"
    else
        echo "service stop failed, please check you privilleges"
    fi
}

status(){
    worker_num=`ps -ef|grep gunicorn|grep -v grep|wc -l`
    if [ $worker_num == 0 ]
    then
        echo "service not running !"
    else
        echo "service is running !"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: ./run.sh start|stop|status"
        ;;
esac
exit 0
