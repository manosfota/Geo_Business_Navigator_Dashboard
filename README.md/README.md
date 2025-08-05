# Geo Business Navigator Intelligence Dashboard

This project combines **Python**, **MySQL**, **SQL queries**, and **Tableau** to create a Geo-Business Intelligence Dashboard. It allows users to:

- Analyze business categories and areas
- Visualize KPIs and geospatial data
- Use interactive Tableau visualizations

## 🔧 Technologies Used

- Python (Data Extraction & Analysis)
- MySQL (Database)
- Tableau (Dashboards)
- Git & GitHub (Version Control)

## 📁 Project Structure

```
Geo_Business_Navigator_Dashboard/
│
├── src/
│   └── geo_business_dashboard.py   # All SQL queries and Python logic
│
├── Tableau_images/
│   ├── Query_1.png
│   ├── Query_2.png
│   └── ...                         # Visuals from Tableau
│
├── geo_business_data.csv          # (Optional) Exported data from MySQL
└── README.md                      # Project overview
```

## 📊 Sample Dashboards

![Query 1](Tableau_images/Query_1.png)
![Query 2](Tableau_images/Query_2.png)

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/manosfota/Geo_Business_Navigator_Dashboard.git
   ```

2. Set up your MySQL database and fill in your `db_config` in `geo_business_dashboard.py`.

3. Run the queries via Python:
   ```bash
   python src/geo_business_dashboard.py
   ```

4. Open Tableau and use the `.csv` file or MySQL connection to create dashboards.
