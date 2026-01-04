#!/bin/bash
print_status() {
    local color=$1
    local message=$2
    case $color in
        "green") echo -e "\e[32m$message\e[0m" ;;
        "red") echo -e "\e[31m$message\e[0m" ;;
        "yellow") echo -e "\e[33m$message\e[0m" ;;
    esac
}

print_status "yellow" "Starting Docker installation process..."

# Remove old Docker versions
print_status "yellow" "Removing old Docker packages if they exist..."
sudo apt-get remove -y docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc &>/dev/null

# Update package index and install prerequisites
print_status "yellow" "Installing prerequisites..."
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# Setup Docker repository
print_status "yellow" "Setting up Docker repository..."
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
print_status "yellow" "Adding Docker repository..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
print_status "yellow" "Installing Docker packages..."
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Setup user permissions
print_status "yellow" "Setting up user permissions..."
sudo usermod -aG docker $USER

# Verify installation
print_status "yellow" "Verifying Docker installation..."
if ! sudo docker run hello-world &>/tmp/docker-test.log; then
    print_status "red" "✘ Docker verification failed. Check the following logs:"
    print_status "yellow" "Docker test output: cat /tmp/docker-test.log"
    print_status "yellow" "System logs: sudo journalctl -u docker.service"
    print_status "yellow" "Docker daemon logs: docker info"
    exit 1
fi

print_status "green" "✔ Docker installation verified successfully!"
print_status "green" "Please log out and back in, or run: newgrp docker"