## **Troubleshooting**

Deployments can encounter issues. Below are common problems and their solutions.

1. **Service Not Starting**

   - **Check Logs**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml logs <service_name>
     ```
   - **Example**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml logs r2r
     ```

2. **Database Connection Issues**

   - **Verify Environment Variables**: Ensure `R2R_POSTGRES_HOST`, `R2R_POSTGRES_PORT`, `R2R_POSTGRES_USER`, and `R2R_POSTGRES_PASSWORD` are correct.
   - **Check Service Status**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml ps
     ```

3. **Healthchecks Failing**

   - **Inspect Health Status**:
     ```bash
     docker inspect --format='{{json .State.Health}}' <container_name>
     ```
   - **Restart Services**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml restart <service_name>
     ```

4. **API Not Responding**

   - **Ensure R2R is Running**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml ps
     ```
   - **Check Network Connectivity**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml exec r2r ping postgres
     ```

5. **Token Generation Issues**

   - **Verify `setup-token` Service Logs**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml logs setup-token
     ```
   - **Ensure `hatchet_api_key` Volume is Mounted Correctly**

6. **Nginx Proxy Issues**

   - **Check Nginx Configuration**: Ensure `nginx.conf` correctly routes traffic.
   - **Reload Nginx**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml exec nginx nginx -s reload
     ```

7. **Unstructured Service Failures**

   - **Check Dependencies**: Ensure all system dependencies are installed.
   - **Inspect Logs**:
     ```bash
     docker-compose -f compose.full_with_replicas.yaml logs unstructured
     ```

---