# Data Explorer API

This README provides complete instructions for setting up and deploying the `Data Explorer` API, which allows users to upload CSV files and query the data using filters. It also includes API usage documentation.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Setup](#setup)
  - [Local Setup](#local-setup)
  - [Remote Setup](#remote-setup)
- [Configuration](#configuration)
- [API Usage](#api-usage)
  - [Endpoints](#endpoints)
- [Example Usage](#example-usage)
- [Cost Estimations](#cost-estimations)

---

## Getting Started

The following sections detail how to set up the application locally or deploy it remotely using Docker and Render.com.

---

## Setup

### Local Setup

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/Santhosh-Chidambaram/data-explorer.git
    cd data-explorer
    ```

2. **Create and Activate a Virtual Environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

4. **Create Environment Variables File:**
   
   Create a `.env` file in the project root with the following content:
   
    ```env
    cp .env.example .env
    ```

5. **Run the Application:**

    ```sh
    (venv)$ python main.py
    ```

6. **Test at:** [http://localhost:8081/docs](http://localhost:8081/docs)

---

### Remote Setup

To deploy the application remotely, follow these steps:

1. **Build a Docker Image:**

    ```sh
    docker build -t <docker_username>/<container_name>:<tag> .
    ```

    Example:

    ```sh
    docker build -t santhoshr02/data-explorer:v0 .
    ```

2. **Push the Image to Docker Registry:**

    ```sh
    docker push <docker_username>/<container_name>:<tag>
    ```

    Example:

    ```sh
    docker push santhoshr02/data-explorer:v0
    ```

3. **Deploy to Render.com:**
   - Log in to [Render](https://render.com).
   - Create a new **Web Service**.
   - Use the Docker image from your registry.
   - Configure the environment variables as in the `.env` file.
   - Deploy the application.

4. **Access Your Deployed Application:**
   - The deployed app will be accessible at the URL provided by Render.

---

## Configuration

The application uses environment variables for configuration. Update the `.env` file to modify settings.

- **`ENVIRONMENT`**: Enviroment.
- **`DB_HOST`**: Clickhouse DB Host.
- **`DB_USER`**: Clickhouse DB User.
- **`DB_PASSWORD`**: Clickhouse DB password.

---

## API Usage

### Endpoints

#### 1. **Upload CSV**

**Endpoint:**
```
POST /data-explorer/upload-csv
```

**Description:**
Uploads a CSV file from the specified URL to be processed and stored for querying.

**Request Body:**
```json
{
    "csv_url": "https://example.com/your-csv-file.csv"
}
```

**Response:**
- **Success:**
  ```json
  {
      "status": 200,
      "message": "CSV uploaded and processed successfully."
  }
  ```
- **Error:**
  ```json
  {
      "status": 400,
      "message": "Failed to upload CSV. Please check the URL."
  }
  ```

---

#### 2. **Query Data**

**Endpoint:**
```
POST /data-explorer/query
```

**Description:**
Queries the uploaded data using filters on specific columns.

**Request Body:**
```json
{
    "filters": [
        {
            "column": "release_date",
            "value": "2011-01-06",
            "operation": "gt"
        }
    ]
}
```

**Supported Operations:**
- `eq` - Equals
- `like` - Contains search substr search
- `lt` - Less than
- `gt` - Greater than
- `lte` - Less than or equal to
- `gte` - Greater than or equal to

**Response:**
- **Success:**
  ```json
  {
      "status": "success",
      "data": [
           {
            "id": "1e1a24d8-0cce-42ed-b19a-07766e2d6c55",
            "appid": 12140,
            "name": "Max Payne",
            "release_date": "2011-01-06",
            "required_age": 17,
            "price": "3.49",
            "dlc_count": 0,
            "about_the_game": "Max Payne is a man with nothing to lose in the violent, cold urban night. A fugitive undercover cop framed for murder, hunted by cops and the mob, Max is a man with his back against the wall, fighting a battle he cannot hope to win. Max Payne is a relentless story-driven game about a man on the edge, fighting to clear his name while struggling to uncover the truth about his slain family amongst a myriad of plot-twists and twisted thugs in the gritty bowels of New York during the century's worst blizzard. The groundbreaking original cinematic action-shooter, Max Payne introduced the concept of Bullet Time® in videogames. Through its stylish slow-motion gunplay combined with a dark and twisted story, Max Payne redefined the action-shooter genre.",
            "supported_languages": [
                "English"
            ],
            "windows": true,
            "mac": false,
            "linux": false,
            "positive": 9516,
            "negative": 1114,
            "score_rank": 0,
            "developers": "Remedy Entertainment",
            "publishers": "Rockstar Games",
            "categories": "Single-player",
            "genres": "Action",
            "tags": "Action,Noir,Classic,Third-Person Shooter,Bullet Time,Story Rich,Atmospheric,Dark,Third Person,Singleplayer,Shooter,Great Soundtrack,Detective,Cinematic,Linear,Crime,Violent,Adventure,Horror,Psychological Horror",
            "created_at": "2024-12-13"
        },
      ]
  }
  ```
---

### Example Usage

1. Use the **Upload CSV** endpoint to process your CSV file.
2. Query the uploaded data using the **Query Data** endpoint with specific filters.

---

---

## **Cost Estimations**

#### **Assumptions**

- **Average Queries Per Day**: 100 queries.
- **Development Environment**: Active for 8 hours daily.
- **Render.com Deployment**: Server hosted on Render.com for additional application needs.
- **Pricing Model**: Based on ClickHouse's usage-based pricing model, including separate scaling of compute and storage resources.


#### **ClickHouse Development Service**
- **Compute Costs**:
  - Active Usage: 4 hours daily.
  - Monthly Compute Costs: $30 - $50 (30 days).

- **Storage Costs**:
  - Assumed included in development pricing unless data volumes exceed typical thresholds for moderate workloads.

#### **Render.com Deployment**
- Server hosted on Render.com for application deployment.
- **Estimated Costs**: $0 per month (Free plan is  sufficent).

#### **Cost Optimization Factors**
- If the 100 daily queries are executed in fewer than 8 hours, compute resource utilization would scale down, reducing the overall cost.
- Leveraging serverless auto-scaling further minimizes costs during idle periods.

---

### **Summary of Estimated Costs**
| **Category**         | **Cost (USD)**  |
|----------------------|-----------------|
| Development Compute  | $30 - $50       |
| Render.com Server    | $0             |
| **Total Estimated**  | **$30 - $50**   |

---


For further details, we can check the official [ClickHouse Pricing Guide](https://clickhouse.com/pricing).
