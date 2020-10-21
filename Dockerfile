FROM python:alpine as master_players_dump_env

# Installing from files for better readability
COPY requirements.txt /
RUN pip install -r /requirements.txt

FROM master_players_dump_env as master_players_dump_pro

COPY run_parser.py .
COPY run_parser.sh .

CMD ./run_parser.sh
