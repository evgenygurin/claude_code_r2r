## **Initial Setup Steps**

After deploying the services, perform the following initial setup steps to configure Hatchet and R2R.

### **Creating the Hatchet API Token**

The `setup-token` service is responsible for generating the Hatchet API token, which R2R uses to communicate with Hatchet.

1. **Ensure `setup-token` Service is Running**

   The `setup-token` service should have already been started by Docker Compose. Verify its status:

   ```bash
   docker-compose -f compose.full_with_replicas.yaml ps
   ```

2. **Verify Token Generation**

   The token is stored in the `hatchet_api_key` volume. To retrieve the token:

   ```bash
   docker exec -it <r2r_container_name> cat /hatchet_api_key/api_key.txt
   ```

   Replace `<r2r_container_name>` with the actual container name, which can be found using:

   ```bash
   docker-compose -f compose.full_with_replicas.yaml ps
   ```

3. **Set Hatchet API Token Environment Variable**

   Ensure that the `HATCHET_CLIENT_TOKEN` environment variable is correctly set in the `r2r` service. This is handled automatically by the `r2r` service command, which reads the token from the `hatchet_api_key` volume.

---