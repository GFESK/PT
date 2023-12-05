FROM gfesk/pt_test_base_img:base

COPY inference.py ./root
COPY utils.py ./root
COPY config.json ./root

WORKDIR /root

CMD [ "python", "./inference.py"]

EXPOSE 8080