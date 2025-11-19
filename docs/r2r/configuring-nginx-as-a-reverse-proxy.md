## **Configuring Nginx as a Reverse Proxy**

Nginx serves as a reverse proxy, directing incoming traffic to the appropriate services based on the configuration in `nginx.conf`.

### **Sample `nginx.conf`**

Ensure you have an `nginx.conf` file in your project root with appropriate proxy settings. Here's a basic example:

```nginx
worker_processes 1;

events { worker_connections 1024; }

http {
    server {
        listen 80;

        location /api/ {
            proxy_pass http://r2r:7272/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /dashboard/ {
            proxy_pass http://r2r-dashboard:3000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /hatchet-dashboard/ {
            proxy_pass http://hatchet-dashboard:80/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location / {
            proxy_pass http://nginx:80/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

> **Customization**: Modify `nginx.conf` according to your routing needs. Ensure that service names in `proxy_pass` match the service names defined in Docker Compose.

### **Reloading Nginx Configuration**

After updating `nginx.conf`, reload Nginx to apply changes:

```bash
docker-compose -f compose.full_with_replicas.yaml exec nginx nginx -s reload
```

---