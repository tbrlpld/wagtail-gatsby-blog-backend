FROM nginx
COPY default.conf /etc/nginx/conf.d/default.conf
COPY set-data-dir-owner.sh /docker-entrypoint.d/set-data-dir-owner.sh
RUN chmod +x /docker-entrypoint.d/set-data-dir-owner.sh