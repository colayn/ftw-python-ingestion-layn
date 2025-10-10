import ibis
import pandas as pd

# 1. Connect to the SQLite Chinook database
con = ibis.sqlite.connect("data/chinook.db")

# 2. Inspect available tables (optional)
print(con.list_tables())
# -> ['albums', 'artists', 'customers', 'employees', 'genres', 'invoices', 'invoice_items', 'tracks', ...]

# 3. Reference the invoices and customers tables
invoices = con.table("invoices")
customers = con.table("customers")

# 4. Join customers and invoices on customer_id
joined = invoices.join(customers, invoices.CustomerId == customers.CustomerId)

# 5. Group by Country and compute average invoice total
result_expr = (
    joined.group_by(joined.Country)
          .aggregate(avg_invoice=joined.Total.mean())
          .order_by(ibis.desc("avg_invoice"))
)

# 6. Execute query and get a pandas DataFrame
df = result_expr.execute()

# 7. Save to CSV
df.to_csv("output/avg_invoice_by_country.csv", index=False)

print("✅ Saved:", df.head())
