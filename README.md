# Customer Segmentation System

An end-to-end Flask web application that categorizes mall customers into distinct behavioral segments using a pre-trained K-Means Machine Learning model.

## Features
- User Authentication (Registration, Login, Session Management with password hashing)
- Pre-trained ML pipeline integration (`StandardScaler` and `K-Means`)
- Output Mapping: Cluster Label -> Description -> Actionable Strategy Recommendation
- SQLite persistent storage for user accounts and historical predictions
- Analytics dashboard comparing model evaluation metrics (Silhouette Score, Davies-Bouldin, Calinski-Harabasz)

## How to Run locally

1. **Activate Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate