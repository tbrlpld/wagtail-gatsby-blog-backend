FROM nginx
COPY default.conf /etc/nginx/conf.d/default.conf
# Add script to set owner of /code/data directory to nginx
# This is to avoid 403 errors where nginx can not serve the file. Nginx is 
# running as the nginx user. Therefore, this user needs access.
COPY set-data-dir-owner.sh /docker-entrypoint.d/set-data-dir-owner.sh
RUN chmod +x /docker-entrypoint.d/set-data-dir-owner.sh