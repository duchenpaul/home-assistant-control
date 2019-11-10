APP_NAME=homebridge_midware_app

cat>Dockerfile<<EOF
FROM python:3.8
ADD ${APP_NAME} /app
WORKDIR /app/FlaskApp
RUN pip install --trusted-host pypi.douban.com -i http://pypi.douban.com/simple -r /app/requirements.txt 
RUN pip install --trusted-host pypi.douban.com -i http://pypi.douban.com/simple gunicorn
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "${APP_NAME}:app"]
EOF

CONTAINER_EXCHANGE_DIR=/app/logs
HOST_EXCHANGE_DIR=~/${APP_NAME}_docker_share
mkdir -p ${HOST_EXCHANGE_DIR}

sudo docker build --tag ${APP_NAME} .
sudo docker save ${APP_NAME} | gzip -c > ${APP_NAME}.tar.gz

APP_NAME=homebridge_midware_app
# sudo docker load < ${APP_NAME}.tar
sudo docker images ${APP_NAME}
sudo docker run -p 5050:5000 --name ${APP_NAME}_ins -v ${HOST_EXCHANGE_DIR}:${CONTAINER_EXCHANGE_DIR} ${APP_NAME}