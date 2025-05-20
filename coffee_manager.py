import multiprocessing
import time
import webbrowser
import random
from datetime import datetime
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from flask import Flask

# Global variables
dash_process = None
DEFAULT_FILE_PATH = 'coffeesales.xlsx'

#Global sales Data
# Valid Items
store_options = {
    1: 'Downtown',
    2: 'Suburbs',
    3: 'Mall',
    4: 'Lower Manhattan',
    5: "Hell's Kitchen"
}
products = [
    {'id': 32, 'name': 'Gourmet Brewed Coffee', 'category': 'Coffee', 'price': 3},
    {'id': 57, 'name': 'Brewed Chai Tea', 'category': 'Tea', 'price': 3.1},
    {'id': 59, 'name': 'Hot Chocolate', 'category': 'Drinking Chocolate', 'price': 4.5},
    {'id': 22, 'name': 'Drip Coffee', 'category': 'Coffee', 'price': 2},
    {'id': 77, 'name': 'Scone', 'category': 'Bakery', 'price': 3},
    {'id': 39, 'name': 'Barista Espresso', 'category': 'Coffee', 'price': 4.25},
    {'id': 51, 'name': 'Brewed Black Tea', 'category': 'Tea', 'price': 3},
    {'id': 47, 'name': 'Brewed Green Tea', 'category': 'Tea', 'price': 3},
    {'id': 42, 'name': 'Brewed Herbal Tea', 'category': 'Tea', 'price': 2.5},
    {'id': 69, 'name': 'Biscotti', 'category': 'Bakery', 'price': 3.25},
    {'id': 71, 'name': 'Pastry', 'category': 'Bakery', 'price': 3.75},
    {'id': 26, 'name': 'Organic Brewed Coffee', 'category': 'Coffee', 'price': 3},
    {'id': 34, 'name': 'Premium Brewed Coffee', 'category': 'Coffee', 'price': 2.45},
    {'id': 64, 'name': 'Regular Syrup', 'category': 'Flavours', 'price': 0.8},
    {'id': 12, 'name': 'Herbal Tea', 'category': 'Loose Tea', 'price': 8.95},
    {'id': 6, 'name': 'Gourmet Beans', 'category': 'Coffee beans', 'price': 21},
    {'id': 9, 'name': 'Organic Beans', 'category': 'Coffee beans', 'price': 28},
    {'id': 65, 'name': 'Sugar Free Syrup', 'category': 'Flavours', 'price': 0.8},
    {'id': 19, 'name': 'Drinking Chocolate', 'category': 'Packaged Chocolate', 'price': 6.4},
    {'id': 7, 'name': 'Premium Beans', 'category': 'Coffee beans', 'price': 19.75},
    {'id': 17, 'name': 'Chai Tea', 'category': 'Loose Tea', 'price': 9.5},
    {'id': 10, 'name': 'Green Beans', 'category': 'Coffee beans', 'price': 10},
    {'id': 4, 'name': 'Espresso Beans', 'category': 'Coffee beans', 'price': 20.45},
    {'id': 15, 'name': 'Green Tea', 'category': 'Loose Tea', 'price': 9.25},
    {'id': 20, 'name': 'Organic Chocolate', 'category': 'Packaged Chocolate', 'price': 7.6},
    {'id': 83, 'name': 'Mugs', 'category': 'Merch', 'price': 14},
    {'id': 13, 'name': 'Black Tea', 'category': 'Loose Tea', 'price': 8.95},
    {'id': 2, 'name': 'House Blend Beans', 'category': 'Coffee beans', 'price': 18},
    {'id': 81, 'name': 'Clothing', 'category': 'Merch', 'price': 28}
]

def load_data(FILE_PATH):
    expected_columns = ["transaction_id", "transaction_date", "transaction_time", "store_id",
                        "store_location", "product_id", "unit_price", "product_category",
                        "product_type", "transaction_qty"]
    valid_product_ids = set({p['id']: p for p in products})
    valid_store_ids = set(store_options.keys())
    valid_store_locations = set(store_options.values())
    valid_prices = set({p['price']: p for p in products})

    # checks if columns are missing
    try:
        data = pd.read_excel(FILE_PATH)
        if not all(col in data.columns for col in expected_columns):
            print(f"Error: Missing columns in {FILE_PATH}. Adding expected columns.")
            return pd.DataFrame(columns=expected_columns)

        valid_rows = []
        invalid_rows = []
        invalid_count = 0

        # checks each row in sheet for invalid data
        for index, row in data.iterrows():
            if row.isnull().any():
                invalid_count += 1
                invalid_rows.append((index, "Contains null values"))
                continue

            try:
                # Basic validation
                datetime.strptime(str(row['transaction_date']), '%m/%d/%Y')
                datetime.strptime(str(row['transaction_time']), '%H:%M:%S')


                # Convert values for comparison
                transaction_id = int(float(row['transaction_id']))
                store_id = int(float(row['store_id']))
                product_id = int(float(row['product_id']))
                unit_price = (row['unit_price'])
                transaction_qty = int(float(row['transaction_qty']))
                store_location = str(row['store_location']).strip()
                product_category = str(row['product_category']).strip()
                product_type = str(row['product_type']).strip()

            #determines validity
                if (transaction_id > 0 and
                        store_id in valid_store_ids and
                        store_location in valid_store_locations and
                        product_id in valid_product_ids and
                        unit_price in valid_prices and
                        product_category and
                        product_type and
                        transaction_qty > 0):
                    valid_rows.append(row)
                else:

                #assings reasons to error
                    reason = ""
                    if transaction_id <= 0:
                        reason = f"Invalid transaction ID: {transaction_id}"
                    elif store_id not in valid_store_ids:
                        reason = f"Invalid store ID: {store_id}"
                    elif store_location not in valid_store_locations:
                        reason = f"Invalid store location: '{store_location}'"
                    elif product_id not in valid_product_ids:
                        reason = f"Invalid product ID: {product_id}"
                    elif unit_price not in valid_prices:
                        reason = f"Invalid unit price: {unit_price}"
                    elif not product_category:
                        reason = "Empty product category"
                    elif not product_type:
                        reason = "Empty product type"
                    elif transaction_qty <= 0:
                        reason = f"Invalid transaction quantity: {transaction_qty}"

                    #counts invalid rows
                    invalid_count += 1
                    invalid_rows.append((index, reason))
            except (ValueError, TypeError) as e:
                invalid_count += 1
                invalid_rows.append((index, f"Error processing row: {e}"))

        print(f"Found {invalid_count} invalid rows")

        # Print info about invalid rows to help debugging
        if invalid_rows:
            print("\nInvalid rows details:")
            for idx, reason in invalid_rows[:10]:  # Show first 10 invalid rows
                print(f"Row {idx + 1}: {reason}")
            if len(invalid_rows) > 10:
                print(f"...and {len(invalid_rows) - 10} more invalid rows")

        return pd.DataFrame(valid_rows)

    except Exception as e:
        print(f"Failed to load {FILE_PATH}: {e}. Starting with empty data.")
        return pd.DataFrame(columns=expected_columns)

def perform_analysis(data,FILE_PATH):
    try:
        #Calculate Metrics
        total_sales = data['transaction_qty'].sum()
        top_drink = data.groupby('product_type')["transaction_qty"].sum().idxmax()
        top_location = data.groupby("store_location")["transaction_qty"].sum().idxmax()
        total_sales_bylocation = data.groupby("store_location")["transaction_qty"].sum()
        average_qty_pertransaction = data['transaction_qty'].mean()
        data['revenue'] = data['transaction_qty'] * data['unit_price']
        total_revenue = data['revenue'].sum()
        top_product_revenue = data.groupby('product_type')['revenue'].sum().idxmax()
        data['hour'] = pd.to_datetime(data['transaction_time'],format='%H:%M:%S').dt.hour
        peak_hour = data.groupby('hour')['transaction_qty'].sum().idxmax()

        # Show results
        print("\nBrew Empire Summary:")
        print(f"Total items sold: {total_sales}")
        print(f"Top drink by units: {top_drink}")
        print(f"Top product by revenue: {top_product_revenue}")
        print(f"Top Location: {top_location}")
        print(f"Total Revenue: ${total_revenue:.2f}")
        print(f"Peak sales hour: {peak_hour}:00")

        #Analysis Suggestions
        #location sales
        mean_sales = total_sales_bylocation.mean()
        for location, sales in total_sales_bylocation.items():
            if sales > mean_sales * 1.3:
                percent_diff = ((sales - mean_sales) / mean_sales) * 100
                print(f"{location} is outperforming by {percent_diff:.1f}% — consider adding more inventory or staff.")
            elif sales < mean_sales * 0.6:
                percent_diff = ((mean_sales - sales) / mean_sales) * 100
                print(f"{location} is underperforming by {percent_diff:.1f}% — investigate reason for low sales.")

        #Transaction Qty
        if average_qty_pertransaction < 2:
            print(f'Average item quantity per transaction is only {average_qty_pertransaction:.2f}. '
                  f'Consider creating bundle deals to encourage larger purchases.')
        else:
            print(f'Average item quantity per transaction is {average_qty_pertransaction:.2f} which is above recommended target. '
                  f'Great Job Boss!')

        input("\nPress Enter to return to menu..")

    except Exception as e:
        print(f"Error with {FILE_PATH}: Missing Data Required {e}")
        print('if invalid sales, clear in developer menu.')
        print(f'Have you added any sales?')

        input("\nPress Enter to return to menu..")

def add_sales(data, FILE_PATH):

    sales_data = []
    running = True
    while running:

        amt_sales_received = False
        while not amt_sales_received:
            print('\nEnter [0] to exit')
            sales_entries = input('How many Sales would you lke to add? (Rows in sheet)' )

            if not sales_entries.isdigit():
                print('Please enter a whole number.')
            else:
                sales_entries = int(sales_entries)
                if int(sales_entries) == 0:
                    amt_sales_received = True
                    running = False
                elif int(sales_entries) < 0:
                    print('Please enter a positive number.')
                else:
                    amt_sales_received = True

        if not data.empty:
            transaction_id = data['transaction_id'].max()
        else:
            transaction_id = 0

        for index in range(sales_entries):
            transaction_id += 1
            print(f"\n--- Entry {index + 1} of {sales_entries} ---")

            #Store Menu
            store_valid = False
            while not store_valid:
                print('\nSelect Location of Sale:')
                print("[0] EXIT")
                for key, val in store_options.items():
                    print(f"[{key}] {val}")


            #Getting Store Value
                store_choice = input('Select Store: ').strip()
                store_choice = int(store_choice)
                if store_choice == '0':
                    if sales_entries > 1:
                        choice = input("Are you sure you would like to exit? You have multiple Entries. Exiting will not save data.(y/n)")
                        if choice.lower() == 'y':
                            print('Exiting Add Sale.')
                            store_valid = True
                            running = False
                    else:
                        store_valid = True
                        running = False
                else:
                    if store_choice in store_options:
                        store = store_options.get(store_choice)
                        store_id = int(store_choice)
                        store_valid = True
                    else:
                        print('Invalid Store Option, Please try again.')

            if not running:
                break

            # Getting Category Value
            drink_valid = False
            while not drink_valid:

                print('\nSelect Product Category:')
                print("[0] --EXIT--")
                category_list = []
                for items in products:
                    category = items['category']
                    category_list.append(category)

                category_list = list(set(category_list))
                for index, category in enumerate(category_list):
                    print(f'[{index + 1}] {category}')

                category_choice = input('Select Category: ').strip()
                if category_choice == '0':
                    if sales_entries > 1:
                        choice = input("Are you sure you would like to exit? You have multiple Entries. Exiting will not save data.(y/n)")
                        if choice.lower() == 'y':
                            print('Exiting Add Sale.')
                            drink_valid= True
                            running = False
                    else:
                        drink_valid = True
                        running = False
                else:
                    if category_choice.isdigit() and int(category_choice) <= len(category_list):
                        product_category = category_list[int(category_choice) - 1]
                        drink_valid = True
                    else:
                        print('Invalid Category option, Please try again.')

            # Getting Product type Value
            product_valid = False
            while not product_valid:

                print('\nSelect Product:')
                print("[0] --EXIT--")
                filtered_products = [items for items in products if items['category'] == product_category]
                for index, items in enumerate(filtered_products):
                    print(f'[{index + 1}] {items["name"]}')

                product_choice = input('Select Product: ').strip()
                if product_choice == '0':
                    if sales_entries > 1:
                        choice = input("Are you sure you would like to exit? You have multiple Entries. Exiting will not save data.(y/n)")
                        if choice.lower() == 'y':
                            print('Exiting Add Sale.')
                            product_valid= True
                            running = False
                    else:
                        product_valid = True
                        running = False
                else:
                    if product_choice.isdigit() and int(product_choice) <= len(filtered_products):
                        selected_product = filtered_products[int(product_choice) - 1]
                        product_name = selected_product['name']
                        product_price = selected_product['price']
                        product_id = selected_product['id']
                        product_valid = True
                    else:
                        print('Invalid Product option, Please try again.')

            if not running:
                break
            #Getting Quantity Value
            quantity_valid = False
            while not quantity_valid:
                quantity = input("Enter quantity sold: ").strip()
                if not quantity.isdigit():
                    print('Quantity must be a number.')
                elif int(quantity) <= 0:
                    print('Quantity must be a positive number.')
                else:
                    quantity_valid = True
                    quantity = int(quantity)

            #Getting Date Value
            date_valid = False
            while not date_valid:
                month = input("Enter Month of Sale (MM): ").strip()
                day = input("Enter Day of Sale (DD): ").strip()
                if not (month.isdigit() and day.isdigit()):
                    print('Month and day must be numbers.')
                    continue
                month, day = int(month), int(day)
                if not (1 <= month <= 12):
                    print('Invalid Month option, Please try again within 01-12.')
                    continue
                try:
                    transaction_date = datetime.strptime(f'{month:02d}/{day:02d}/2025', '%m/%d/%Y').strftime('%m/%d/%Y')
                    date_valid = True
                except ValueError:
                    print(f'Invalid date: {month:02d}/{day:02d}/2025. Please try again.')

            random_hour = random.randint(7, 20)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            transaction_time = (f'{random_hour:02d}:{random_minute:02d}:{random_second:02d}')

        if running:
            # Add new sale to the DataFrame
            sales_data.append([transaction_id, transaction_date, transaction_time, store_id, store, product_id, product_price, product_category, product_name, quantity])
            new_sale = pd.DataFrame(sales_data, columns=(["transaction_id","transaction_date","transaction_time","store_id","store_location","product_id","unit_price","product_category","product_type","transaction_qty"]))
            data = pd.concat([data, new_sale], ignore_index=True)
            print(f"Added: {quantity} Sale(s) at {store}")
            try:
                print('Saving data')
                data.to_excel(FILE_PATH, index=False)
                print(f"Saved data to {FILE_PATH}")
            except Exception as e:
                print(f"Error saving to {FILE_PATH}: {e}")
        else:
            break

    running = False
    return data

def generate_random_sale(data, sale_quantity, FILE_PATH, simulate_trend=False):

    transactions = [
        {'transaction_id': 0, 'transaction_date': '1/1/2025', 'transaction_time': '07:15'}
    ]

    category_weights = {
        'Coffee': 58,
        'Tea': 45,
        'Bakery': 25,
        'Drinking Chocolate': 20,
        'Coffee beans': 11,
        'Merch': 6,
        'Flavours': 10,
        'Packaged Chocolate': 6,
        'Loose Tea': 8
    }

    # Sale Quantity range
    low_range = [1, 2]
    med_range = [3, 4]
    high_range = [5, 6]

    if not data.empty:
        transaction_id = data['transaction_id'].max()
    else:
        transaction_id = 0

    # List to hold the sale data
    sales_data = []

    #Simulate Trend
    trend_month = None
    trend_product = None
    if simulate_trend:
        trend_month = random.randint(1,12)
        trend_product = random.choice(products)
        print(f"Simulating trend: {trend_product['name']} in month {trend_month}")

    # Generate random sales according to sale_quantity
    for _ in range(sale_quantity):
        store_id = random.choice(list(store_options.keys()))
        store = store_options[store_id]
        store_id = int(store_id)

        product_weights = []
        #getting random product based on weighted category choice
        for product in products:
            category = product['category']
            weight = category_weights[category]
            product_weights.append(weight)

        if simulate_trend and random.random() < 0.5:
            trend_index = products.index(trend_product)
            product_weights[trend_index] = 100


        random_product = random.choices(products, weights=product_weights)[0]
        product_id = random_product['id']
        product_name = random_product['name']
        product_category = random_product['category']
        product_price = random_product['price']

        transaction_id += 1

        #set trend month 70% of time
        if simulate_trend and random.random() < 0.7:
            random_month = trend_month
        else:
        # monthly random based on popularity of the year
            month_set = [(1,2),(3,5),(6,7),(8,9),(10,12)]
            chosen_month_range = random.choices(month_set, weights = [1.0,1,0.9,1.2,1.4])[0]
            random_month = random.randint(chosen_month_range[0],chosen_month_range[1])

        #calculates day based on gregorian calendar
        if random_month == 2:
            random_day = random.randint(1, 28)
        elif random_month in [4,6,9,11]:
            random_day = random.randint(1, 30)
        else:
            random_day = random.randint(1, 31)

        # Random Date within 2025 and Time within open hours
        random_hour = random.randint(7, 20)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        random_date = (f'{random_month:02d}/{random_day:02d}/2025')
        random_time = (f'{random_hour:02d}:{random_minute:02d}:{random_second:02d}')
        transaction_date = random_date
        transaction_time = random_time

        # Random sale quantity
        range_choice = random.choices([low_range, med_range, high_range], weights=[0.96, 0.03, 0.01])[0]
        quantity = random.choice(range_choice)

        # Add the sale data to the list
        sales_data.append([transaction_id, transaction_date, transaction_time, store_id, store, product_id, product_price, product_category, product_name, quantity])

    # Convert the lists into a dataframe and add new sales to existing data frame
    new_sales_df = pd.DataFrame(sales_data, columns=["transaction_id","transaction_date","transaction_time","store_id","store_location","product_id","unit_price","product_category","product_type","transaction_qty"])
    if data.empty:
        data = new_sales_df
    else:
        data = pd.concat([data, new_sales_df], ignore_index=True)

    # Save the updated data to Excel
    try:
        print(f"Saving to: {FILE_PATH}")
        data.to_excel(FILE_PATH, index=False)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving to {FILE_PATH}: {e}")

    return data

def clear_data(FILE_PATH):
    # Add new sale to the DataFrame
    clear_file = pd.DataFrame(columns=["transaction_id","transaction_date","transaction_time","store_id","store_location","product_id","unit_price","product_category","product_type","transaction_qty"])
    try:
        clear_file.to_excel(FILE_PATH, index=False)
        print(f"Saved data to {FILE_PATH}")
    except Exception as e:
        print(f"Error saving to {FILE_PATH}: {e}")

    return clear_file

def run_dashboard(data):

    try:
        #converts string date to datetime format
        data['transaction_date'] = pd.to_datetime(data['transaction_date'], format='%m/%d/%Y')

        #caluculation metrics
        total_sales = data["transaction_qty"].sum()
        unique_products = data["product_id"].nunique()
        total_transactions = data["transaction_id"].nunique()
        top_product = data.groupby('product_type')['transaction_qty'].sum().idxmax()

        #groups sum of sales by date and converts to date time
        df_total = data.groupby('transaction_date').agg({'transaction_qty': 'sum'}).reset_index()

        #sorts sales by date
        df_total = df_total.sort_values('transaction_date')
        mean_sales = df_total['transaction_qty'].mean()

        #calculates total revenue, creates monthly transaction column, and calculates monthly revenue
        data['revenue'] = data['transaction_qty'] * data['unit_price']
        monthly_revenue = data.groupby(data['transaction_date'].dt.month)['revenue'].sum().reset_index()

        # Add month names
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_revenue['month'] = monthly_revenue['transaction_date'].map(lambda x: month_names[x - 1])


        bar_chart = px.bar(data_frame=data.groupby('product_type').agg({'transaction_qty': 'sum'}).reset_index(),
                           x='product_type', y='transaction_qty', title="Units Sold by Product Type", template="plotly_dark",color_discrete_sequence=['#004953'])
        pie_chart = px.pie(data_frame=data.groupby('product_category').agg({'transaction_qty': 'sum'}).reset_index(),
                           names='product_category', values='transaction_qty', title="Sales by Product Category", template="plotly_dark",color_discrete_sequence=['#004953'])
        line_chart = px.line(data_frame=df_total,
                             x='transaction_date', y='transaction_qty', title="Sales By Date", template="plotly_dark", color_discrete_sequence=['#004953'])
        line_chart.add_hline(y=mean_sales, line_dash="dash", line_color="#00CED1",
                                   annotation_text=f"Mean: {mean_sales:.1f}",
                                   annotation_position="top left")
        monthly_revenue_line_chart = px.line(data_frame=monthly_revenue,x='month', y='revenue', title="Total Revenue by Month",
            template="plotly_dark", color_discrete_sequence=['#004953'],
            labels={'transaction_date': 'Month', 'total_revenue': 'Total Revenue ($)'})

        server = Flask(__name__)
        app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.CYBORG])
        app.title = "Coffee Intelligence Dashboard"
        app.layout = dbc.Container([
            html.H1("☕ Coffee Intelligence Dashboard", className="text-center mb-4",style={"color": "#00CED1"}),
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Total Units Sold"),
                    dbc.CardBody(html.H5(f"{total_sales}", className="card-title"))
                ], color="dark", inverse=True), width=4),
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Unique Products"),
                    dbc.CardBody(html.H5(f"{unique_products}", className="card-title"))
                ], color="dark", inverse=True), width=4),
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Total Transactions"),
                    dbc.CardBody(html.H5(f"{total_transactions}", className="card-title"))
                ], color="dark", inverse=True), width=4),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(html.H4(f"🧠 Top-selling product: {top_product}",style={"color": "#00CED1"}))
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(html.P("Consider bundling it or featuring it in promotions."))
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=bar_chart), md=6),
                dbc.Col(dcc.Graph(figure=pie_chart), md=6)
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=line_chart))
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=monthly_revenue_line_chart))
            ], className="mb-4")

        ], fluid=True)
        webbrowser.open("http://127.0.0.1:8050")
        app.run(debug=True, use_reloader=False, port=8050)
    except Exception as e:
        print(f"Missing Required Data! {e}")
        print('--wait--')

def start_dashboard(data):
    global dash_process
    # Start new Dash process
    dash_process = multiprocessing.Process(target=run_dashboard, args=(data,))
    dash_process.daemon = True
    dash_process.start()
    time.sleep(5)

def stop_dash_server():
    global dash_process
    print('Stopping Dashboard server.')
    if dash_process is not None and dash_process.is_alive():
        dash_process.terminate()
        dash_process.join(timeout=2.0)
        if dash_process.is_alive():
            print("Warning: Dash process did not terminate cleanly")
        dash_process = None

def view_sales(data):
    print("\nCurrent sales:")
    try:
        if not data.empty:
            print(data)
        else:
            print("No sales yet—add some!")
    except Exception as e:
        print(f"Error reading {FILE_PATH}: {e}")

def developer_menu(data, FILE_PATH):

    dev_menu = True
    while dev_menu:
        print("\nWelcome to Developer Options.")
        print("These are used to showcase the tools in the program with custom scenarios.")
        print("Select What You'd like To Do:")
        print("\n[0] Exit")
        print("[1] Add 100 Random Sales")
        print("[2] Add 1000 Random Sales")
        print("[3] Add 50,000 Random Sales !WARNING! Processes may take longer. ")
        print("[4] Add 1000 sales that simulate trending product in random month")
        print("[5] Load Sample Datasets")
        print("[6] Clear Data")
        choice = input(f'SELECT OPTION: ')

        # menu directory
        if choice == '1':
            print("Adding 100 Random Sales...")
            data = generate_random_sale(data, 100, FILE_PATH)
            print("Done.")
        elif choice == '2':
            print("Adding 1,000 Random Sales...")
            data = generate_random_sale(data, 1000, FILE_PATH)
            print("Done.")
        elif choice == '3':
            data = generate_random_sale(data, 50000, FILE_PATH)
            print("Done.")
        elif choice == '4':
            data = generate_random_sale(data, 1000, FILE_PATH, simulate_trend=True)
        elif choice == '5':
            running = True
            while running:
                print('[0] Back')
                print("[1] Switch to default.")
                oneortwo = input('[2] Switch to pre-loaded realistic coffee sales ')
                if oneortwo == '0':
                    running = False
                elif oneortwo == '1':
                    FILE_PATH = DEFAULT_FILE_PATH
                    print(f'Loading data at {FILE_PATH}')
                    data = load_data(FILE_PATH)
                    running = False
                elif oneortwo == '2':
                    FILE_PATH = 'realistic_data.xlsx'
                    print(f'Loading data at {FILE_PATH}')
                    try:
                        data = load_data(FILE_PATH)
                    except FileNotFoundError:
                        print(f'ERROR. {FILE_PATH} not found, starting with empty set.')
                    running = False
                else:
                    print('invalid input. Please enter 0, 1 or 2.')
        elif choice == '6':
            yesorno = input('Are you sure you would like to clear all data (y/n)')
            if yesorno.lower() == 'y':
                data = clear_data(FILE_PATH)
            elif yesorno.lower() == 'n':
                pass
            else:
                print("Please enter y or n.")


        elif choice == '0':
            print("Exiting Developer Options!")
            dev_menu = False
        else:
            print("INVALID OPTION. Please choose 0, 1, 2, 3")

    return data, FILE_PATH

def welcome_menu(data, FILE_PATH):
    if data is None:
        print("Error: Data could not be loaded. Exiting.")
        return None

    running = True
    while running:
        print("\nWelcome Boss to Your Brew Empire Business Manager!")
        print("Select What You'd like To Do:")
        print("\n[0] Exit")
        print("[1] View Sales")
        print("[2] Add Sales")
        print("[3] Dashboard")
        print("[4] Perform Business Analysis")
        print("[5] Developer Menu")
        choice = input('SELECT OPTION: ')


        if choice == '1':
            view_sales(data)
        elif choice == '2':
            data = add_sales(data, FILE_PATH)
        elif choice == '3':
            print("\nLaunching dashboard...")
            start_dashboard(data)
            input("\nPress 'Enter' to return to the menu...")
            stop_dash_server()
        elif choice == '4':
            perform_analysis(data,FILE_PATH)
        elif choice == '5':
            data,FILE_PATH = developer_menu(data, FILE_PATH)
        elif choice == '0':
            print("Exiting Business Manager!")
            running = False
        else:
            print("INVALID OPTION. Please choose 0, 1, 2, 3, 4, or 5")

    return data, FILE_PATH

# Check if data is None before proceeding
if __name__ == "__main__":
    print('*make sure excel file is closed before editing*')
    print('---LOADING DATA ----')
    FILE_PATH = DEFAULT_FILE_PATH
    data = load_data(FILE_PATH)
    if data is None:
        print("Failed to initialize data. Exiting program.")
    else:
        print("Data loaded.")
        data,FILE_PATH = welcome_menu(data, FILE_PATH)
        if data is not None:
            try:
                print('---SAVING DATA---')
                data.to_excel(FILE_PATH, index=False)
                print(f"Data saved to {FILE_PATH}")
            except Exception as e:
                print(f"Error saving data to {FILE_PATH}: {e}")