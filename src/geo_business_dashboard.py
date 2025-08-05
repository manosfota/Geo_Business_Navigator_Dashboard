import random
import pymysql
import pandas as pd
from faker import Faker
from geopy.distance import geodesic
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

fake=Faker()

business_categories=[
  "Cafeteria", "Gym", "Super Market", "Hair Salon", 
   "Pharmacy", "Bookstore", "Restaurant", "Patisserie"
]

areas=[
  "Dublin", "Maynooth", "Lucan", "Bray",
  "Howth", "Naas", "Cork", "Mullingar","Navan"
]

# ======================
# 🔹Step 1: Create Date
# ======================
def generate_fake_businesses(n=100):
  data=[]
  for _ in range(n):
    name=fake.company()
    category=random.choice(business_categories)
    area=random.choice(areas)

    latitude = round(random.uniform(53.30, 53.40), 6)
    longitude = round(random.uniform(-6.30, -6.20), 6)


    open_hours=random.randint(7,11)
    close_hours=random.randint(17, 23)
    opening_hours=f"{open_hours}:00-{close_hours}:00"

    data.append({
      "Business Name": name,
      "Category": category,
      "Area": area,
      "Latitude": latitude,
      "Longitude": longitude,
      "Opening Hours": opening_hours
    })

  df=pd.DataFrame(data)
  print(df)
  return df

# =============================
# 🔹Step 2: Time Preprocessing
# =============================
def preprocess_opening_hours(df):
  df[['Open Hour', 'Close Hour']]=df['Opening Hours'].str.extract(r'(\d+):\d+\s*-\s*(\d+):\d+')
  df['Open Hour']=df['Open Hour'].astype(int)
  df['Close Hour']= df['Close Hour'].astype(int)
  df['Is_Open_After_20']=df['Close Hour']>20
  return df 
 
# =============================================
# 🔹Step 3: Distance from the center of Dublin
# ============================================= 
def add_distance_from_center(df, center_coords=(53.349805, -6.26031)):
  distances=[]
  for idx, row in df.iterrows():
    business_coords=(row['Latitude'], row['Longitude'])
    distance_km=round(geodesic(center_coords, business_coords).km, 2)
    distances.append(distance_km)

  df['Distance_km_from_Dublin_Center']=distances
  return df


# ========================================================
# 🔹Step 4: Create MySQL DB (if not exists) & Upload Data
# ========================================================
def load_dataframe_to_mysql(df, table_name, db_config):
  host=db_config['host']
  user=db_config['user']
  password=db_config['password']
  database=db_config['database']

  # Step A : Create DB if not exists  
  try:
    connection=pymysql.connect(host=host,user=user,password=password)
    cursor=connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    print(f"✅ Database {database} has already created")
  except pymysql.MySQLError as e:
    print("❌ Error! Database didn't create")
    print(e)
  finally:
    cursor.close()
    connection.close()

  # Step B: Load dataframe to MySQL
  try:
    engine=create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"✅Data uploaded to table '{table_name}' successfully.")
  except SQLAlchemyError as e:
    print("❌ Error uploading data:", e)


# ================================================
# 🔹Step 5: Common function for executing a query
# ================================================
def execute_query(query, db_config):
  engine=create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
  try:
    df=pd.read_sql(query, con=engine)
    return df
  except Exception as e:
    print("❌ Error executing query:", e)
    return None


# 🔸 Query 1:
# ===========
def get_business_count_by_category(db_config):

  query="""
      SELECT Category, Count(*) AS Business_Count
      FROM businesses
      GROUP BY Category
      ORDER BY Business_Count DESC;
"""
  return execute_query(query, db_config)


# 🔸 Query 2:
# ===========
def get_businesses_open_after_20(db_config):
  query="""
      SELECT `Business Name`, Category, `Close Hour`
        FROM businesses
        WHERE Is_Open_After_20 = TRUE;
    """
  return execute_query(query, db_config)


# 🔸 Query 3:
# ===========
def get_business_count_by_area(db_config):
    query = """
        SELECT Area, COUNT(*) AS Business_Count
        FROM businesses
        GROUP BY Area
        ORDER BY Business_Count DESC;
    """
    return execute_query(query, db_config)


# 🔸 Query 4:
# ===========
def get_businesses_within_5km(db_config):
    query = """
        SELECT `Business Name`, Distance_km_from_Dublin_Center
        FROM businesses
        WHERE Distance_km_from_Dublin_Center < 5;
    """
    return execute_query(query, db_config)


# 🔸 Query 5:
# ===========
def get_top_3_categories(db_config):
    query = """
        SELECT Category, COUNT(*) AS Business_Count
        FROM businesses
        GROUP BY Category
        ORDER BY Business_Count DESC
        LIMIT 3;
    """
    return execute_query(query, db_config)


# 🔸 Query 6:
# ============
def get_top_3_areas(db_config):
    query = """
        SELECT Area, COUNT(*) AS Business_Count
        FROM businesses
        GROUP BY Area
        ORDER BY Business_Count DESC
        LIMIT 3;
    """
    return execute_query(query, db_config)


# 🔸 Query 7
# ===========
def get_area_business_distribution(db_config):
    query = """
        SELECT Area, COUNT(*) AS Business_Count
        FROM businesses
        GROUP BY Area
        ORDER BY Business_Count DESC;
    """
    return execute_query(query, db_config)


# 🔸 Query 8
# ===========
def get_category_business_count_with_alias(db_config):
  query="""
      SELECT Category, Count(*) As Business_Count
      FROM businesses
      GROUP BY Category
      ORDER BY Business_Count DESC;
""" 
  return execute_query(query, db_config)


# 🔸 Query 9
# ===========
def get_category_sorted_ascending(db_config):
    query = """
        SELECT Category, COUNT(*) AS Business_Count
        FROM businesses
        GROUP BY Category
        ORDER BY Category ASC;
    """
    return execute_query(query, db_config)


# 🔸 Query 10
# ============
def get_area_sorted_desc(db_config):
    query = """
        SELECT Area, COUNT(*) AS Business_Count
        FROM businesses
        GROUP BY Area
        ORDER BY Area DESC;
    """
    return execute_query(query, db_config)



# ==================
# 🔹Step 5: Run All 
# ==================
def main():
  # Function 1: Generate Fake Business Data
  df=generate_fake_businesses(100)

  # Function 2: Preprocess Opening Hours
  df=preprocess_opening_hours(df)

  # Function 3: Add Distance from Dublin Center
  df=add_distance_from_center(df)

  # Function 4: Preview first 20 rows
  print(df.head(20))

  # Function 5: Save to CSV locally
  df.to_csv("geo_business_data.csv", index=False)

  # Function 6: Database credentials
  db_config={
    "host":"localhost",
    "user":"root",
    "password":"Manos1231!",
    "database":"geo_business_db"
  }

  # Function 7: Load DataFrame to MySQL
  load_dataframe_to_mysql(df=df,table_name="businesses",db_config=db_config)


  #     🔸🔸 Run SQL Queries 🔸🔸
  print("\n🔹 Query 1: Business Count by Category:")
  print(get_business_count_by_category(db_config))

  print("\n🔹 Query 2: Businesses Open After 20:00:")
  print(get_businesses_open_after_20(db_config))

  print("\n🔹 Query 3: Top 3 Categories:")
  print(get_top_3_categories(db_config))

  print("\n🔹 Query 4: Top 3 Areas with Most Businesses:")
  print(get_top_3_areas(db_config))

  print("\n🔹 Query 5: Businesses Within 5km from Dublin Center:")
  print(get_businesses_within_5km(db_config))

  print("\n🔹 Query 6: Business Count by Area:")
  print(get_business_count_by_area(db_config))

  print("\n🔹 Query 7: Area Business Distribution:")
  print(get_area_business_distribution(db_config))

  print("\n🔹 Query 8: Category Business Count with Alias:")
  print(get_category_business_count_with_alias(db_config))

  print("\n🔹 Query 9: Category Sorted Ascending:")
  print(get_category_sorted_ascending(db_config))

  print("\n🔹 Query 10: " \
  "")
  print(get_area_sorted_desc(db_config))

 
if __name__=='__main__':
  main()



