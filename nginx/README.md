# Nginx

## generate key/cert command

- openssl req -new -sha256 -newkey rsa:2048 -nodes -keyout local.key -x509 -days 365 -out local.crt
