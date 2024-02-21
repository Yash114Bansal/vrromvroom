FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils\
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    postgis*

RUN apt update && apt install postgis -y

# Set GDAL library path
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
