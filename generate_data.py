import pandas as pd
import random
from datetime import datetime, timedelta

def generate_sample_data(num_rows=150):
    regions = {
        'North': ['Delhi', 'Chandigarh', 'Jaipur'],
        'South': ['Bangalore', 'Chennai', 'Hyderabad'],
        'East': ['Kolkata', 'Patna', 'Bhubaneswar'],
        'West': ['Mumbai', 'Pune', 'Ahmedabad']
    }
    categories = ['Electronics', 'Clothing', 'Home Appliances', 'Books', 'Furniture']
    modes = ['Road', 'Air', 'Train']
    statuses = ['Delivered', 'Delayed', 'In Transit', 'Cancelled']
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_rows):
        order_date = start_date + timedelta(days=random.randint(0, 180))
        region = random.choice(list(regions.keys()))
        city = random.choice(regions[region])
        mode = random.choice(modes)
        
        expected_days = 2 if mode == 'Air' else (5 if mode == 'Road' else 7)
        expected_delivery = order_date + timedelta(days=expected_days)
        
        status = random.choices(statuses, weights=[0.6, 0.2, 0.1, 0.1])[0]
        
        if status == 'Delivered':
            actual_days = expected_days - random.randint(0, 1)
        elif status == 'Delayed':
            actual_days = expected_days + random.randint(1, 5)
        else: 
            actual_days = None
            
        delivery_date = order_date + timedelta(days=actual_days) if actual_days else None
        shipping_cost = random.randint(50, 500) if mode == 'Road' else (random.randint(500, 1500) if mode == 'Air' else random.randint(100, 800))
        
        rating = random.randint(1, 5) if status in ['Delivered', 'Delayed'] else None
        if random.random() < 0.05:
            rating = None
        if random.random() < 0.05:
            shipping_cost = None
            
        data.append({
            'Shipment_ID': f'SHP{1000 + i}',
            'Order_Date': order_date.strftime('%Y-%m-%d'),
            'Delivery_Date': delivery_date.strftime('%Y-%m-%d') if delivery_date else None,
            'Customer_ID': f'CUST{random.randint(100, 999)}',
            'Region': region,
            'City': city,
            'Product_Category': random.choice(categories),
            'Quantity': random.randint(1, 20),
            'Transportation_Mode': mode,
            'Shipping_Cost': shipping_cost,
            'Delivery_Status': status,
            'Expected_Delivery_Days': expected_days,
            'Actual_Delivery_Days': actual_days,
            'Delivery_Rating': rating
        })
        
    df = pd.DataFrame(data)
    df.to_excel('sample_logistics_data.xlsx', index=False)
    print("Successfully generated sample_logistics_data.xlsx")

if __name__ == '__main__':
    generate_sample_data()
