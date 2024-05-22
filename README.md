# IMS App Backend Codebase

To run the backend server:
1. Copy the `.env.*.example` files to `.env.*` and fill in the necessary environment variables.

    Or use the `init.sh` script.
2. Run `docker compose up --build -d` to start the server.
3. APIs will be available at `http://localhost`.
4. To check all APIs docs, visit `http://localhost/docs`.
5. To stop the server, run `docker compose down`.