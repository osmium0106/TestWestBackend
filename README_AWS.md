# AWS EC2 Django Deployment Guide

## 1. Connect to Your EC2 Instance

1. Make sure your EC2 instance is running and note its public IPv4 address (e.g., `13.60.81.50`).
2. Ensure your security group allows SSH (port 22) from your IP.
3. Open a terminal on your local machine and run:
   ```sh
   ssh -i "C:/Users/91812/Downloads/Testwest.pem" ubuntu@<your-ec2-public-ip>
   ```
   - Replace `<your-ec2-public-ip>` with your instance's public IP.
   - Type `yes` if prompted about authenticity.

---

## 2. Initial Setup (First Time Only)

On your EC2 instance:

1. Update and install dependencies:
   ```sh
   sudo apt update
   sudo apt install -y git docker.io docker-compose
   sudo usermod -aG docker ubuntu
   exit
   ```
   Then reconnect via SSH.

2. Clone your project:
   ```sh
   git clone https://github.com/osmium0106/TestWestBackend.git
   cd TestWestBackend
   ```

3. Build and run Docker:
   ```sh
   sudo docker-compose up -d --build
   ```

4. Run Django migrations and collect static files:
   ```sh
   sudo docker-compose exec web python manage.py migrate
   sudo docker-compose exec web python manage.py collectstatic --noinput
   ```

5. (Optional) Create a Django superuser:
   ```sh
   sudo docker-compose exec web python manage.py createsuperuser
   ```

---

## 3. Deploying Code Changes from Local to AWS

Whenever you make changes to your code locally and want to update your AWS deployment:

1. **Commit and push your changes to GitHub:**
   ```sh
   git add .
   git commit -m "Describe your changes"
   git push
   ```

2. **SSH into your EC2 instance:**
   ```sh
   ssh -i "C:/Users/91812/Downloads/Testwest.pem" ubuntu@<your-ec2-public-ip>
   cd TestWestBackend
   ```

3. **Pull the latest code:**
   ```sh
   git pull
   ```

4. **Rebuild and restart Docker containers:**
   ```sh
   sudo docker-compose down -v
   sudo docker-compose up -d --build
   ```

5. **Run migrations and collect static files (if needed):**
   ```sh
   sudo docker-compose exec web python manage.py migrate
   sudo docker-compose exec web python manage.py collectstatic --noinput
   ```

---

## 4. Accessing Your App

- Open your browser and go to:
  - `http://<your-ec2-public-ip>:8000/` (for Django dev server)
  - Or the port you configured for production.

---

## 5. Troubleshooting

- **Permission denied (publickey):** Check your `.pem` file path and permissions, and ensure your EC2 security group allows SSH.
- **Connection timed out:** Check that your instance is running, has a public IP, and security group allows port 22.
- **App not updating:** Make sure you `git pull` and rebuild Docker containers after pushing changes.

---

**Tip:** For production, consider using Nginx, HTTPS, and environment variables for security and performance.
