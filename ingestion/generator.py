"""
Synthetic E-Commerce Data Generator for Indian Marketplace Big Data Analytics.
Generates realistic Customers, Products, Orders, Order Items, and Web Clickstream events in INR (₹).
"""

import uuid
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path
from config.settings import DATA_DIR
from utils.logger import get_logger

try:
    from faker import Faker
    fake = Faker('en_IN')  # Indian locale for realistic names and addresses
    Faker.seed(42)
except ImportError:
    fake = None

np.random.seed(42)
random.seed(42)

logger = get_logger("DataGenerator")

# Indian E-Commerce Product Categories with Realistic Price Ranges in INR (₹)
CATEGORY_PRICE_RANGES = {
    "Electronics": {
        "sub_categories": ["Smartphones", "Laptops", "Audio & Headphones", "Smartwatches", "Cameras", "Accessories"],
        "min_price": 500.0,
        "max_price": 150000.0
    },
    "Fashion & Apparel": {
        "sub_categories": ["Men's Clothing", "Women's Clothing", "Footwear", "Ethnic Wear", "Accessories"],
        "min_price": 300.0,
        "max_price": 15000.0
    },
    "Home & Kitchen": {
        "sub_categories": ["Furniture", "Kitchenware", "Home Decor", "Bedding & Linen", "Appliances"],
        "min_price": 200.0,
        "max_price": 50000.0
    },
    "Beauty & Personal Care": {
        "sub_categories": ["Skincare", "Haircare", "Makeup", "Fragrances", "Personal Hygiene"],
        "min_price": 100.0,
        "max_price": 10000.0
    },
    "Grocery & Daily Needs": {
        "sub_categories": ["Staples & Grains", "Beverages", "Snacks", "Dairy & Bakery", "Packaged Food"],
        "min_price": 50.0,
        "max_price": 5000.0
    },
    "Books & Stationery": {
        "sub_categories": ["Fiction", "Non-Fiction", "Competitive Exams", "Academic", "Stationery"],
        "min_price": 100.0,
        "max_price": 5000.0
    },
    "Sports & Fitness": {
        "sub_categories": ["Fitness Equipment", "Sports Gear", "Activewear", "Outdoor & Camping"],
        "min_price": 200.0,
        "max_price": 30000.0
    }
}

INDIAN_STATES_CITIES = [
    ("Mumbai", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Chennai", "Tamil Nadu"),
    ("Kolkata", "West Bengal"),
    ("Ahmedabad", "Gujarat"),
    ("Pune", "Maharashtra"),
    ("Jaipur", "Rajasthan"),
    ("Lucknow", "Uttar Pradesh"),
    ("Chandigarh", "Punjab"),
    ("Kochi", "Kerala")
]

PAYMENT_METHODS = ["UPI (Google Pay / PhonePe / Paytm)", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery (COD)"]
ORDER_STATUSES = ["Delivered", "Delivered", "Delivered", "Shipped", "Processing", "Cancelled"]
EVENT_TYPES = ["page_view", "page_view", "product_view", "add_to_cart", "remove_from_cart", "checkout_start", "purchase_complete"]

def generate_customers(num_customers: int = 500) -> pd.DataFrame:
    customers = []
    start_date = datetime.now() - timedelta(days=730)
    for i in range(1, num_customers + 1):
        cid = f"CUST_{i:05d}"
        name = fake.name() if fake else f"Customer {i}"
        email = fake.email() if fake else f"user{i}@example.in"
        city, state = random.choice(INDIAN_STATES_CITIES)
        country = "India"
        signup_dt = start_date + timedelta(days=random.randint(0, 700))
        segment = random.choice(["Retail", "Wholesale", "VIP", "Regular"])
        customers.append({
            "customer_id": cid,
            "name": name,
            "email": email,
            "city": city,
            "state": state,
            "country": country,
            "signup_date": signup_dt.strftime("%Y-%m-%d"),
            "customer_segment": segment
        })
    return pd.DataFrame(customers)

def generate_products(num_products: int = 150) -> pd.DataFrame:
    products = []
    cat_names = list(CATEGORY_PRICE_RANGES.keys())
    for i in range(1, num_products + 1):
        pid = f"PROD_{i:04d}"
        cat = random.choice(cat_names)
        cat_info = CATEGORY_PRICE_RANGES[cat]
        sub_cat = random.choice(cat_info["sub_categories"])
        p_name = f"{sub_cat} Item {i}"
        
        # Log-uniform distribution for realistic INR pricing
        min_p = cat_info["min_price"]
        max_p = cat_info["max_price"]
        price = round(np.exp(random.uniform(np.log(min_p), np.log(max_p))), 2)
        cost = round(price * random.uniform(0.6, 0.85), 2)
        stock = random.randint(15, 600)

        products.append({
            "product_id": pid,
            "product_name": p_name,
            "category": cat,
            "sub_category": sub_cat,
            "unit_price": price,
            "cost_price": cost,
            "stock_quantity": stock
        })
    return pd.DataFrame(products)

def generate_orders_and_items(customers_df: pd.DataFrame, products_df: pd.DataFrame, num_orders: int = 3500):
    orders = []
    order_items = []
    
    cust_ids = customers_df["customer_id"].tolist()
    cust_city_map = dict(zip(customers_df["customer_id"], customers_df["city"]))
    prod_ids = products_df["product_id"].tolist()
    prod_price_map = dict(zip(products_df["product_id"], products_df["unit_price"]))
    
    start_date = datetime.now() - timedelta(days=365)
    item_seq = 1

    for i in range(1, num_orders + 1):
        oid = f"ORD_{i:06d}"
        cid = random.choice(cust_ids)
        ord_date = start_date + timedelta(days=random.randint(0, 364), minutes=random.randint(0, 1439))
        pay_method = random.choice(PAYMENT_METHODS)
        city = cust_city_map.get(cid, "Mumbai")
        status = random.choice(ORDER_STATUSES)
        
        # 1 to 5 items per order
        num_items = random.randint(1, 5)
        selected_prods = random.sample(prod_ids, num_items)
        order_total = 0.0

        for pid in selected_prods:
            item_id = f"ITEM_{item_seq:07d}"
            item_seq += 1
            qty = random.randint(1, 4)
            unit_price = prod_price_map[pid]
            discount = round(unit_price * qty * random.choice([0.0, 0.0, 0.05, 0.10, 0.15]), 2)
            item_total = round((unit_price * qty) - discount, 2)
            order_total += item_total

            order_items.append({
                "item_id": item_id,
                "order_id": oid,
                "product_id": pid,
                "quantity": qty,
                "unit_price": unit_price,
                "discount_amount": discount,
                "total_price": item_total
            })

        orders.append({
            "order_id": oid,
            "customer_id": cid,
            "order_date": ord_date.strftime("%Y-%m-%d %H:%M:%S"),
            "payment_method": pay_method,
            "shipping_city": city,
            "order_status": status,
            "total_amount": round(order_total, 2)
        })

    return pd.DataFrame(orders), pd.DataFrame(order_items)

def generate_clickstream(customers_df: pd.DataFrame, num_events: int = 12000) -> pd.DataFrame:
    events = []
    cust_ids = customers_df["customer_id"].tolist()
    start_date = datetime.now() - timedelta(days=180)
    categories = list(CATEGORY_PRICE_RANGES.keys())

    for i in range(1, num_events + 1):
        ev_id = f"EVT_{i:08d}"
        cid = random.choice(cust_ids)
        session_id = f"SES_{random.randint(1000, 9999)}"
        event_type = random.choice(EVENT_TYPES)
        page = f"/catalog/{random.choice(categories).lower().replace(' ', '_')}"
        ev_dt = start_date + timedelta(days=random.randint(0, 179), minutes=random.randint(0, 1439))
        
        events.append({
            "event_id": ev_id,
            "customer_id": cid,
            "session_id": session_id,
            "event_type": event_type,
            "page_url": page,
            "event_timestamp": ev_dt.strftime("%Y-%m-%d %H:%M:%S")
        })

    return pd.DataFrame(events)

def generate_all_datasets(output_dir: Path = DATA_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Starting Indian Marketplace synthetic dataset generation in INR (₹)...")

    cust_df = generate_customers(num_customers=500)
    prod_df = generate_products(num_products=150)
    orders_df, items_df = generate_orders_and_items(cust_df, prod_df, num_orders=3500)
    clicks_df = generate_clickstream(cust_df, num_events=12000)

    # Save to CSV
    cust_df.to_csv(output_dir / "customers.csv", index=False)
    prod_df.to_csv(output_dir / "products.csv", index=False)
    orders_df.to_csv(output_dir / "orders.csv", index=False)
    items_df.to_csv(output_dir / "order_items.csv", index=False)
    clicks_df.to_csv(output_dir / "web_clickstream.csv", index=False)

    logger.info(f"Datasets successfully generated in '{output_dir}':")
    logger.info(f"- Customers: {len(cust_df)} rows")
    logger.info(f"- Products: {len(prod_df)} rows (INR prices: ₹{prod_df['unit_price'].min()} to ₹{prod_df['unit_price'].max()})")
    logger.info(f"- Orders: {len(orders_df)} rows (Total Revenue: ₹{orders_df['total_amount'].sum():,.2f})")
    logger.info(f"- Order Items: {len(items_df)} rows")
    logger.info(f"- Clickstream Events: {len(clicks_df)} rows")

if __name__ == "__main__":
    generate_all_datasets()
