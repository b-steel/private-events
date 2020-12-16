FROM python:3.8-alpine

# set workdir
WORKDIR /usr/src/app

# install requirements
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project 
COPY . .

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]


