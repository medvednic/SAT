FROM python:3
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN \ 
  pip install -r requirements.txt && \
  python -m textblob.download_corpora && \
  chmod +x sat.sh
	
EXPOSE 5000

CMD ["sh", "./sat.sh"]