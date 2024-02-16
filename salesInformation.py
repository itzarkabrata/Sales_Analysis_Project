import pandas as pd
import os
from matplotlib import pyplot as plt
from itertools import combinations
from collections import Counter

#all month datas are present in this data-frame
all_month_data = pd.DataFrame();

for files in os.listdir("./Sales_Data"):
    df = pd.read_csv(f"./Sales_Data/{files}")
    all_month_data = pd.concat([all_month_data,df]);
    
    
all_month_data.to_csv("./Output/whole_data.csv",index=False)


#this is the overall dataframe
all_data = pd.read_csv("./Output/whole_data.csv")

print(all_data.head())


#Below are the datacleaning processes......

#1) drop all rows that consists NAN values
all_data = all_data.dropna()

print(all_data.head())


#creating a new Month column in which the order is placed

all_data["Month Of Order"] = all_data["Order Date"].str[0:2]

#2) drop all rows that consists some values that are inappropiate

all_data = all_data.loc[all_data["Month Of Order"]!="Or"]

all_data["Month Of Order"] = all_data["Month Of Order"].astype('int16')

print(all_data.head())

#creating a sales column that demonstrate the total amount of purchase on that order

all_data["Quantity Ordered"] = all_data["Quantity Ordered"].astype("int16")
all_data["Price Each"] = all_data["Price Each"].astype("float64")

all_data["Sale Amount"] = all_data["Quantity Ordered"]*all_data["Price Each"]


# on which month the sales is high, I am using matplotlib to visualize this

Total_Sales = all_data.groupby("Month Of Order").sum().loc[:,"Sale Amount"]

months = [i for i in range(1,13)]

month_name = ["January","February","March","April","May","June","July","August","September","October","November","December"]

plt.bar(months,Total_Sales)

plt.title("Total Sales in Each Month")

plt.xticks(months,month_name,rotation="vertical")

plt.xlabel("Months")
plt.ylabel("Total Sales(In Rupees)")

plt.show()

#on which month maximum number of orders are placed

Total_Order = all_data.groupby("Month Of Order").sum().loc[:,"Quantity Ordered"]

plt.bar(months,Total_Order)

plt.title("Total Number of Order in Each Month")

plt.xticks(months,month_name,rotation="vertical")

plt.xlabel("Months")
plt.ylabel("Total Orders (In Units)")

plt.show()

#from which state maximum orders were placed

def extractState(a):
    return a.split(", ")[1] +"["+a.split(", ")[2].split(" ")[0]+"]"


all_data["State"] = all_data["Purchase Address"].apply(extractState)

print(all_data.head())


#group by through states


Total_Sales_per_State = all_data.groupby("State").sum().loc[:,"Sale Amount"]

State_Name = Total_Sales_per_State.keys()

xVals = [i for i in range(0,len(State_Name))]

plt.bar(xVals,Total_Sales_per_State)

plt.xticks(xVals,State_Name,rotation ='vertical')

plt.title("Total amount of sales in Each State")

plt.xlabel("State Names")
plt.ylabel("Total Sales(In Rupees)")

plt.show()


#what is the time of maximum orders so far we can advertise our products at that time to accelorate our businesss

#changing the datatype of Order date to datetime

all_data["Order Date"] = pd.to_datetime(all_data["Order Date"])

# creating Hour and Minute column

all_data["Hours(24)"] = all_data["Order Date"].dt.hour
all_data["Minute"] = all_data["Order Date"].dt.minute

No_of_Orders = all_data.groupby("Hours(24)").count()["Order ID"]

Hours = No_of_Orders.keys()

plt.plot(Hours,No_of_Orders)

plt.grid()

plt.title("Number of order at each hour")

plt.xticks(Hours)

plt.xlabel("Hours in 24")
plt.ylabel("Number of Orders")

plt.show()


# which product sales in large amount

quantity = all_data.groupby("Product").sum()["Quantity Ordered"].astype("int64")

item = quantity.keys()

fig = plt.figure(figsize=(8, 8))
plt.pie(quantity,labels=item)


plt.show()

print(all_data.head())

#find the products that most often ordered together

#creating a new dataframe that consists those products that ordered together
together_orders = all_data[all_data.duplicated("Order ID", keep=False) == True]

together_orders["Ordered Products"] = together_orders.groupby("Order ID")["Product"].transform(lambda x: ','.join(x))

together_orders = together_orders[["Order ID","Ordered Products"]].drop_duplicates()

print(together_orders.head(20))



count = Counter()

for row in together_orders["Ordered Products"]:
    row_list = row.split(",")
    count.update(Counter(combinations(row_list,2)))
    
l = count.most_common()
pair_orders = pd.DataFrame(l,columns=["Pair-Items","Quantity"])

print(pair_orders.head())
