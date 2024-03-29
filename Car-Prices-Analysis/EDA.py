import numpy as np
import pandas as pd
import plotly.express as px

# Load the data from CSV files
df_source = pd.read_csv("./Car-Prices-Analysis/Sources/car_prices.csv")
df_cleaned = pd.read_csv("./Car-Prices-Analysis/Sources/car_prices_cleaned.csv")

# Mapping of color names to Plotly color codes
available_color = ["aliceblue", "antiquewhite", "aqua", "aquamarine", "azure",
                   "beige", "bisque", "black", "blanchedalmond", "blue",
                   "blueviolet", "brown", "burlywood", "cadetblue",
                   "chartreuse", "chocolate", "coral", "cornflowerblue",
                   "cornsilk", "crimson", "cyan", "darkblue", "darkcyan",
                   "darkgoldenrod", "darkgray", "darkgrey", "darkgreen",
                   "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange",
                   "darkorchid", "darkred", "darksalmon", "darkseagreen",
                   "darkslateblue", "darkslategray", "darkslategrey",
                   "darkturquoise", "darkviolet", "deeppink", "deepskyblue",
                   "dimgray", "dimgrey", "dodgerblue", "firebrick",
                   "floralwhite", "forestgreen", "fuchsia", "gainsboro",
                   "ghostwhite", "gold", "goldenrod", "gray", "grey", "green",
                   "greenyellow", "honeydew", "hotpink", "indianred", "indigo",
                   "ivory", "khaki", "lavender", "lavenderblush", "lawngreen",
                   "lemonchiffon", "lightblue", "lightcoral", "lightcyan",
                   "lightgoldenrodyellow", "lightgray", "lightgrey",
                   "lightgreen", "lightpink", "lightsalmon", "lightseagreen",
                   "lightskyblue", "lightslategray", "lightslategrey",
                   "lightsteelblue", "lightyellow", "lime", "limegreen",
                   "linen", "magenta", "maroon", "mediumaquamarine",
                   "mediumblue", "mediumorchid", "mediumpurple",
                   "mediumseagreen", "mediumslateblue", "mediumspringgreen",
                   "mediumturquoise", "mediumvioletred", "midnightblue",
                   "mintcream", "mistyrose", "moccasin", "navajowhite", "navy",
                   "oldlace", "olive", "olivedrab", "orange", "orangered",
                   "orchid", "palegoldenrod", "palegreen", "paleturquoise",
                   "palevioletred", "papayawhip", "peachpuff", "peru", "pink",
                   "plum", "powderblue", "purple", "red", "rosybrown",
                   "royalblue", "rebeccapurple", "saddlebrown", "salmon",
                   "sandybrown", "seagreen", "seashell", "sienna", "silver",
                   "skyblue", "slateblue", "slategray", "slategrey", "snow",
                   "springgreen", "steelblue", "tan", "teal", "thistle", "tomato",
                   "turquoise", "violet", "wheat", "white", "whitesmoke",
                   "yellow", "yellowgreen"
                   ]
color_map = {'Burgundy': 'darkred', 'Charcoal': 'olive', 'Off-White': 'whitesmoke'}
unique_colors = df_cleaned['color'].unique()
for color in unique_colors:
    if color.lower() in available_color:
        color_map[color] = color.lower()


# Functions for first tab (Top Car Brands and Models Analysis)


def top(df, dim, n):
    top_dim = df[dim].value_counts().nlargest(n).index
    top_dim = df[df[dim].isin(top_dim)].reset_index(drop=True)
    fig = px.histogram(top_dim, x=dim, color=dim)
    fig.update_layout(
        title=f'Cars Sold For Each {dim.title()}',
        xaxis_title=dim.title(),
        yaxis_title='Cars Sold',
        title_x=0.35,

    )
    return fig


def top_body_type(df, n):
    top_body = df['body'].value_counts().nlargest(n).index
    top_body = df[df['body'].isin(top_body)].reset_index(drop=True)
    body_counts = top_body['body'].value_counts()
    fig = px.pie(top_body, values=body_counts.values, names=body_counts.index)
    fig.update_layout(
        title='Cars Sold For Each Body Type',
        title_x=0.5
    )
    return fig


def top_colors(df, types, n):
    top_types = df[types].value_counts().nlargest(n).index
    top_types = df[df[types].isin(top_types)].reset_index(drop=True)
    types_counts = top_types[types].value_counts()
    fig = px.pie(top_types, values=types_counts.values, names=types_counts.index, color=types_counts.index,
                  color_discrete_map=color_map)
    fig.update_layout(
        title=f'Cars Sold For Each {types} Type',
        title_x=0.5
    )
    return fig


# Functions for second tab (Total Sales Analysis)

def total_sales_by_type(df, types, n):
    total_sales_types = df.groupby(types)['sellingprice'].sum().reset_index()
    total_sales_types = total_sales_types.nlargest(n, 'sellingprice')
    fig = px.bar(total_sales_types, x=types, y='sellingprice',
                  title=f'Total Sales by Car {types.title()} (Top {n})',
                  labels={'sellingprice': 'Total Sales', f'{types}': f'Car {types}'},
                  color=types)
    fig.update_layout(title_x=0.5)
    return fig


def sales_by_month(df):
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
    monthly_sales = df.groupby('month').size().reset_index(name='count')
    monthly_sales['month'] = pd.Categorical(monthly_sales['month'], categories=month_order, ordered=True)
    monthly_sales = monthly_sales.sort_values('month')
    fig = px.bar(monthly_sales, y='count', x='month',
                  title='Number of Cars Sold on Each Month',
                  color='month')
    fig.update_layout(title_x=0.5)
    return fig


def sales_by_day(df):
    daily_sales = df.groupby('day').size().reset_index(name='count')
    fig = px.pie(daily_sales, values='count', names='day',
                  title='Number of Cars Sold on Each Day', hole=0.4)
    fig.update_layout(title_x=0.5)
    return fig


# Functions for third tab (Price Analysis)

def avg_price(df, dim, n):
    avg_price_dim = df.groupby(dim)['sellingprice'].mean().reset_index()
    avg_price_dim = avg_price_dim.sort_values('sellingprice', ascending=False).head(n)
    fig = px.bar(avg_price_dim, x=dim, y='sellingprice',
                   title=f'Average Selling Price by {dim.title()}',
                   labels={'sellingprice': 'Average Selling Price', dim: dim.title()},
                   color=dim,
                   )
    fig.update_layout(title_x = 0.5)
    return fig


def odo_sell(df):
    fig = px.scatter(df, x='odometer', y='sellingprice',
                       title='Correlation between Odometer Readings and Selling Prices',
                       labels={'odometer': 'Odometer (miles)', 'sellingprice': 'Selling Price'})
    fig.update_layout(title_x=0.5)
    return fig


def cond_sell(df):
    average_selling_price_by_condition = df.groupby('condition')['sellingprice'].mean().reset_index()
    fig = px.line(average_selling_price_by_condition, x='condition', y='sellingprice',
                    title='Relation between Condition and Average Selling Price',
                    labels={'condition': 'Condition', 'sellingprice': 'Average Selling Price'})
    fig.update_layout(title_x=0.5)
    return fig


def col_int_sell(df, dim, n):
    average_selling_price_by_dim = df.groupby(dim)['sellingprice'].mean().reset_index()
    average_selling_price_by_dim = average_selling_price_by_dim.sort_values('sellingprice', ascending=False).head(
        n)
    fig = px.bar(average_selling_price_by_dim,
                   x=dim,
                   y='sellingprice',
                   title=f'Top {n} {dim.title()} by Selling Price',
                   labels={'dim': 'dim', 'sellingprice': 'Average Selling Price'},
                   color=dim,
                   color_discrete_map=color_map)
    fig.update_layout(title_x=0.5)
    return fig


# Functions for fourth tab (Sellers Analysis)

def top_sellers_count(n):
    vehicles_sold_by_seller = df_cleaned['seller'].value_counts().reset_index().head(n)
    vehicles_sold_by_seller.columns = ['seller', 'vehicles_sold']
    fig = px.bar(vehicles_sold_by_seller, x='seller', y='vehicles_sold',
                 title=f'Top {n} Sellers - Cars Sold',
                 color='seller')
    fig.update_layout(xaxis_title='Seller', yaxis_title='Total Number of Vehicles Sold', title_x=0.5)
    return fig


def top_sellers_sales(n):
    sales_by_seller = df_cleaned.groupby('seller')['sellingprice'].sum().reset_index()
    sales_by_seller = sales_by_seller.nlargest(n, 'sellingprice')
    fig = px.bar(sales_by_seller, x='seller', y='sellingprice',
                 title=f'Top {n} Sellers - Total Sales',
                 color='sellingprice')
    fig.update_layout(xaxis_title='Seller', yaxis_title='Total Sales ($)', title_x=0.5)
    return fig


def avg_odometer_seller(n):
    average_odometer_by_seller = df_cleaned.groupby('seller')['odometer'].mean().reset_index()
    average_odometer_by_seller = average_odometer_by_seller.nlargest(n, 'odometer')
    fig = px.bar(average_odometer_by_seller, x='seller', y='odometer',
                 title=f'Top {n} Sellers - Odometer Readings',
                 labels={'seller': 'Seller', 'Odometer': 'Average Odometer', },
                 color='seller',
                 color_continuous_scale='ice')
    fig.update_layout(title_x=0.5)
    return fig


# Functions for fifth tab (State Analysis)

def sales_per_state(n):
    total_revenue_by_state = df_cleaned.groupby('state')['sellingprice'].sum().reset_index().head(n)
    total_revenue_by_state = total_revenue_by_state.sort_values(by='sellingprice', ascending=False)
    fig = px.bar(total_revenue_by_state, x='state', y='sellingprice',
                 title=f'Top {n} States - Sales',
                 labels={'state': 'State', 'sellingprice': 'Total Sales Revenue'},
                 color='state')
    fig.update_layout(title_x=0.5)
    return fig


def condition_state(n):
    average_condition_by_state = df_cleaned.groupby('state')['condition'].mean().reset_index().head(n)
    average_condition_by_state = average_condition_by_state.sort_values('condition', ascending=False)
    fig = px.bar(average_condition_by_state, x='state', y='condition',
                 title=f'Top {n} States - Condition',
                 labels={'state': 'State', 'condition': 'Average Condition'},
                 color='state')
    fig.update_layout(title_x=0.5)
    return fig


def avg_price_state(n):
    avg_price_by_state = df_cleaned.groupby('state')['sellingprice'].mean().reset_index().head(n)
    avg_price_by_state = avg_price_by_state.sort_values('sellingprice', ascending=False)
    fig = px.bar(avg_price_by_state, x='state', y='sellingprice',
                 title=f'Top {n} States - Average Price',
                 labels={'state': 'State', 'sellingprice': 'Average Selling Price'},
                 color='state')
    fig.update_layout(title_x=0.5)
    return fig