# Running as root (or sudoer)
apt-get update
if ! command -v docker &> /dev/null
then 
  echo "Docker not found. Installing..."
  apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg-agent \
      software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
  add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) \
     stable"
  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.i
else
  echo "Docker is already installed"
fi
docker --version

# Install docker-compose
if ! command -v docker-compose &> /dev/null 
then 
  echo "docker-compose not found. Installing..."
  curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
else 
  echo "docker-compose is already installed"
fi
docker-compose --version