# 📊 Customer Analytics Platform (Segment AI)

> An end-to-end Unsupervised Machine Learning web application built with **Flask**, **PostgreSQL**, and **Scikit-Learn** that segments customers into distinct target personas to drive personalized marketing and business strategies.

---

## 📌 Project Overview

**Segment AI** is a data-driven customer intelligence tool that processes demographic and behavioral data (Age, Gender, Annual Income, and Spending Score) to group customers into distinct segments.

Instead of relying on a single default algorithm, the platform evaluates multiple clustering models across industry-standard evaluation metrics and deploys **K-Means Clustering** as the optimal segmentation engine.

---

## ✨ Key Features

* 🔐 **User Authentication**: Secure user registration, password hashing (Werkzeug), and session-based login/logout management.
* 📈 **Interactive Dashboard**: Real-time overview displaying total evaluation count, active segments, algorithm selection, database status, and recent prediction logs.
* 🤖 **Real-time ML Segmentation**: Input customer metrics to immediately determine cluster assignment, segment label, customer characteristics, and actionable recommendations.
* 📊 **Algorithm Analytics & Benchmarking**: Comparison view evaluating model performance across multiple clustering techniques.
* 📜 **Prediction History Log**: Persistent log powered by PostgreSQL storing all historical evaluations.
* ℹ️ **About & Team Page**: Detailed overview of project methodology, ML evaluation metrics, and project contribution credits.

---

## 🛠️ Tech Stack

### **Backend & Database**
* **Language**: Python 3.x
* **Framework**: Flask
* **Database**: PostgreSQL (Render Cloud Managed DB)
* **Database Adapter**: `psycopg2-binary`

### **Machine Learning & Data Science**
* **ML Library**: `scikit-learn`
* **Data Manipulation**: `pandas`, `numpy`
* **Primary Model**: K-Means Clustering ($K = 5$)

### **Frontend & UI**
* **Templates**: Flask Jinja2 HTML Templates
* **Styling**: Modern Custom CSS Grid & Flexbox (Responsive)
* **Icons**: Bootstrap Icons (`bi`)

### **Deployment & Hosting**
* **Cloud Platform**: Render (Web Service & Managed PostgreSQL Database)
* **Version Control**: Git & GitHub

---

## 📐 Machine Learning Methodology & Metrics

The system analyzes customer datasets using four unsupervised clustering algorithms:
1. **K-Means Clustering** *(Selected Model)*
2. **Agglomerative Clustering**
3. **Hierarchical Clustering**
4. **DBSCAN**

### **Evaluation Metrics Used**:
* **Silhouette Score**: Measures cluster cohesion and separation.
* **Davies-Bouldin Index**: Evaluates average similarity between each cluster and its most similar counterpart.
* **Calinski-Harabasz Index**: Ratio of total between-cluster variance to within-cluster variance.
* **Inertia (Within-Cluster Sum of Squares)**: Measures internal cluster closeness (Elbow Method).

*Based on comprehensive benchmarking across these metrics, **K-Means** achieved the highest cluster separation and stability, making it the primary algorithm for predictions.*

---

## 📁 Project Structure

```text
├── app.py                  # Main Flask app & route handlers
├── database.py             # PostgreSQL connection & table initialization
├── predictor.py            # Model inference script for cluster assignments
├── recommendation.py       # Strategic business recommendations mapping
├── requirements.txt        # Python package dependencies
├── Procfile                # Deployment instructions for Render
├── static/                 # Static assets (CSS, JS, Images)
└── templates/              # Jinja2 HTML views
    ├── base.html           # Master layout template & sidebar
    ├── home.html           # Landing page
    ├── login.html          # User login view
    ├── register.html       # User registration view
    ├── dashboard.html      # Main dashboard with stats & recent logs
    ├── predict.html        # Customer input form & result view
    ├── analytics.html      # Model comparison & performance metrics
    ├── history.html        # Database log history table
    └── about.html          # Project details & team information
