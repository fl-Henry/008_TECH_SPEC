echo ""
echo "sudo apt-get update"
sudo apt-get update
echo ""
echo "sudo apt-get install ca-certificates curl gnupg"
sudo apt-get install ca-certificates curl gnupg
echo ""
echo "sudo install -m 0755 -d /etc/apt/keyrings"
sudo install -m 0755 -d /etc/apt/keyrings
echo ""
echo "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo ""
echo "sudo chmod a+r /etc/apt/keyrings/docker.gpg"
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo ""
echo ""
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
echo ""
echo 'sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
echo ""
echo 'sudo apt-get update'
sudo apt-get update
echo ""
echo 'sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin'
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
echo ""
echo 'sudo docker run hello-world'
sudo docker run hello-world