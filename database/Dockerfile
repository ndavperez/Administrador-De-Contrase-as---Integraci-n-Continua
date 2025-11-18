FROM postgres:16-alpine

# Valores por defecto 
ENV POSTGRES_USER=vault \
    POSTGRES_PASSWORD=vaultpass \
    POSTGRES_DB=vaultdb




COPY init/*.sql /docker-entrypoint-initdb.d/

# El entrypoint por defecto de la imagen oficial ya arranca postgres,
# así que no necesitas CMD extra.
