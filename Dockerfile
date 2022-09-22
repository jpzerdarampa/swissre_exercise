FROM python:latest

LABEL Maintainer="JuanPabloZerda"

WORKDIR /usr/app/src

COPY Analyzer.py ./
#COPY access.log ./

ENTRYPOINT ["python" , "./Analyzer.py"]
