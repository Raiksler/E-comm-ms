FROM postgres

ENV POSTGRES_PASSWORD pgadminpass
ENV POSTGRES_DB ecom

COPY ecom_dump.sql /docker-entrypoint-initdb.d/