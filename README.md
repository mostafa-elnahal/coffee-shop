# CoffeeMesh Microservices

## Project Overview

CoffeeMesh is a robust, scalable, and distributed microservices-based application designed to manage a modern coffee shop's operations. This project serves as a practical demonstration of building and integrating independent services, showcasing best practices in API design, data validation, and inter-service communication. It's built with a focus on maintainability, scalability, and resilience, making it an excellent example of a real-world microservices architecture.

## Architecture

CoffeeMesh adopts a microservices architecture, breaking down complex business functionalities into smaller, independent services. This approach allows for independent development, deployment, and scaling of each service, enhancing agility and system resilience.

The core microservices in the CoffeeMesh ecosystem include:

*   **Products Service**: Manages CoffeeMesh’s product catalog, including coffee types, sizes, and pricing.
*   **Orders Service**: Manages customer orders, from creation to tracking.
*   **Payments Service**: Handles secure processing of customer payments.
*   **Kitchen Service**: Manages the production and preparation of orders in the kitchen.
*   **Delivery Service**: Oversees the logistics and tracking of customer deliveries.

## Key Technologies & Design Patterns

This project leverages a modern Python stack and adheres to several key design principles, with specific technologies chosen for each microservice:

### Technologies Used

*   **Python**: The primary programming language for all backend services.
*   **Flask-Smorest & Marshmallow (for Kitchen Service)**:
    *   **Flask-Smorest**: Provides a robust framework for building RESTful APIs, including OpenAPI specification generation.
    *   **Marshmallow**: Utilized for declarative schema definition and powerful data validation and serialization/deserialization, ensuring data integrity.
*   **FastAPI & Pydantic (for Orders Service)**:
    *   **FastAPI**: A modern, fast (high-performance) web framework for building APIs, based on standard Python type hints.
    *   **Pydantic**: Used for data validation and settings management, integrating seamlessly with FastAPI to enforce data schemas.
*   **OpenAPI (Swagger)**: Each microservice is documented with an OpenAPI specification, facilitating clear API contracts and enabling easy integration and testing.

### Design Patterns

*   **Microservices Architecture**: Breaking down the application into small, independent services for scalability, resilience, and maintainability.
*   **RESTful API Design**: Adherence to REST principles for clear, stateless, and resource-oriented API endpoints.
*   **Data Immutability**: Employing deep copies for input data to prevent unintended side effects and ensure predictable function behavior.
*   **Data Standardization**: Consistent use of ISO 8601 format for date-time fields, promoting interoperability and unambiguous data exchange.
*   **Layered Validation**: Implementing multiple layers of validation (schema-based payload validation and post-update business logic validation) to ensure data integrity at various stages of processing.

## Service Details

### Kitchen Service

The Kitchen Service is responsible for managing the lifecycle of orders within the kitchen, from scheduling to completion or cancellation.

**API Endpoints (from `oas.yaml`):**

*   `GET /kitchen/schedules`: Retrieves a list of orders scheduled for production, with optional filtering by `progress`, `limit`, and `since` (date-time).
*   `POST /kitchen/schedules`: Schedules a new order for production.
*   `GET /kitchen/schedules/{schedule_id}`: Returns the status and details of a specific scheduled order.
*   `PUT /kitchen/schedules/{schedule_id}`: Updates an existing scheduled order.
*   `DELETE /kitchen/schedules/{schedule_id}`: Deletes a scheduled order.
*   `GET /kitchen/schedules/{schedule_id}/status`: Returns only the status of a scheduled order.
*   `POST /kitchen/schedules/{schedule_id}/cancel`: Cancels a scheduled order.

**Key Features:**

*   Order scheduling and status management.
*   Robust input and output validation using Marshmallow schemas.
*   Server-side generation of `id` and `scheduled` timestamps for new orders.
*   Clear error handling for "Not Found" scenarios.

### Orders Service

The Orders Service is a critical component for managing the entire lifecycle of customer orders within CoffeeMesh. It handles everything from order creation and retrieval to payment processing and cancellation.

**API Endpoints (from `orders-microservice/oas.yaml`):**

*   `GET /orders`: Retrieves a list of customer orders, with optional filtering by `cancelled` status and `limit`.
*   `POST /orders`: Creates a new customer order.
*   `GET /orders/{order_id}`: Returns the details of a specific order by its ID.
*   `PUT /orders/{order_id}`: Replaces an existing order with new details.
*   `DELETE /orders/{order_id}`: Deletes an existing order.
*   `POST /orders/{order_id}/pay`: Processes payment for a specific order.
*   `POST /orders/{order_id}/cancel`: Cancels an existing order.

**Key Features:**

*   Comprehensive order management (create, retrieve, update, delete).
*   Order status tracking (e.g., `created`, `paid`, `progress`, `cancelled`, `dispatched`, `delivered`).
*   Integration points for payment and kitchen services (via `pay` and `cancel` endpoints).
*   Robust input validation and response serialization using schemas.
*   Secure API endpoints with `openId`, `oauth2`, and `bearerAuth` security schemes.

## Getting Started

(Instructions on how to set up and run the microservices locally will go here.)

## Learning Resources

This project is developed as an educational endeavor, drawing inspiration and guidance from the book **"Microservice APIs: Using Python, Flask, FastAPI, OpenAPI and more" by José Haro Peralta (Manning Publications)**. It serves as a practical application of the concepts and best practices discussed in the book, particularly regarding the implementation of microservices using Python, Flask, FastAPI, and OpenAPI.