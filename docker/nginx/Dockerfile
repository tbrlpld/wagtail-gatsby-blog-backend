FROM nginx
# Create directory owned by user nginx where the data will be mounted
RUN mkdir -p /code/data && chmod -R nginx:nginx /code
COPY default.conf /etc/nginx/conf.d/default.conf