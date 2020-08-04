# Install nginx
if ! command -v nginx &> /dev/null 
then 
  echo "nginx not found. Installing..."
  apt-get install -y nginx
else 
  echo "nginx is already installed"
fi
nginx -v

