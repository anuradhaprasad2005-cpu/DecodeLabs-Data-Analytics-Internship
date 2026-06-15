-- ============================================================
-- DecodeLabs Data Analytics Internship | Batch 2026
-- Project 3: SQL Data Analysis
-- Author  : Anuradha Prasad
-- Dataset : E-Commerce Orders | 1,200 rows x 14 columns
-- Tool    : SQLite (via Python)
-- Date    : June 2026
-- ============================================================

-- TABLE: orders
-- Columns: OrderID, Date, CustomerID, Product, Quantity,
--          UnitPrice, ShippingAddress, PaymentMethod,
--          OrderStatus, TrackingNumber, ItemsInCart,
--          CouponCode, ReferralSource, TotalPrice

-- ============================================================
-- QUERY 01 | SELECT + ORDER BY
-- Business Question: What are the 5 highest-value orders?
-- Clauses Used: SELECT, FROM, ORDER BY DESC, LIMIT
-- ============================================================

SELECT  OrderID,
        CustomerID,
        Product,
        Quantity,
        TotalPrice,
        OrderStatus
FROM    orders
ORDER BY TotalPrice DESC
LIMIT 5;

-- ============================================================
-- QUERY 02 | WHERE (Equality Filter)
-- Business Question: Which orders have been cancelled?
-- Clauses Used: SELECT, FROM, WHERE, ORDER BY
-- ============================================================

SELECT  OrderID,
        CustomerID,
        Product,
        TotalPrice,
        ReferralSource
FROM    orders
WHERE   OrderStatus = 'Cancelled'
ORDER BY TotalPrice DESC;

-- ============================================================
-- QUERY 03 | COUNT + GROUP BY
-- Business Question: How many orders exist per status?
-- Clauses Used: SELECT, COUNT(*), FROM, GROUP BY, ORDER BY
-- ============================================================

SELECT  OrderStatus,
        COUNT(*) AS Total_Orders,
        ROUND(COUNT(*) * 100.0 / 1200, 2) AS Percentage
FROM    orders
GROUP BY OrderStatus
ORDER BY Total_Orders DESC;

-- ============================================================
-- QUERY 04 | SUM + GROUP BY
-- Business Question: Which product generates the most revenue?
-- Clauses Used: SELECT, SUM(), AVG(), COUNT(), FROM, GROUP BY
-- ============================================================

SELECT  Product,
        COUNT(*) AS Total_Orders,
        ROUND(SUM(TotalPrice), 2) AS Total_Revenue,
        ROUND(AVG(TotalPrice), 2) AS Avg_Order_Value
FROM    orders
GROUP BY Product
ORDER BY Total_Revenue DESC;

-- ============================================================
-- QUERY 05 | AVG + GROUP BY
-- Business Question: Which payment method has the highest average order value?
-- Clauses Used: SELECT, AVG(), SUM(), COUNT(), FROM, GROUP BY
-- ============================================================

SELECT  PaymentMethod,
        COUNT(*) AS Total_Orders,
        ROUND(AVG(TotalPrice), 2) AS Avg_Order_Value,
        ROUND(SUM(TotalPrice), 2) AS Total_Revenue
FROM    orders
GROUP BY PaymentMethod
ORDER BY Avg_Order_Value DESC;

-- ============================================================
-- QUERY 06 | WHERE + AND (Multi-Condition Filter)
-- Business Question: Which high-value orders (>2000) were delivered?
-- Clauses Used: SELECT, FROM, WHERE, AND, ORDER BY
-- ============================================================

SELECT  OrderID,
        Product,
        PaymentMethod,
        TotalPrice,
        ReferralSource
FROM    orders
WHERE   TotalPrice > 2000
  AND   OrderStatus = 'Delivered'
ORDER BY TotalPrice DESC;

-- ============================================================
-- QUERY 07 | HAVING (Filter on Grouped Data)
-- Business Question: Which referral channels have more than 240 orders?
-- Clauses Used: SELECT, COUNT(), SUM(), AVG(), GROUP BY, HAVING, ORDER BY
-- Note: HAVING filters AFTER GROUP BY. WHERE filters BEFORE grouping.
-- ============================================================

SELECT  ReferralSource,
        COUNT(*) AS Total_Orders,
        ROUND(SUM(TotalPrice), 2) AS Total_Revenue,
        ROUND(AVG(TotalPrice), 2) AS Avg_Order_Value
FROM    orders
GROUP BY ReferralSource
HAVING  COUNT(*) > 240
ORDER BY Total_Revenue DESC;

-- ============================================================
-- QUERY 08 | Multi-Aggregation (COUNT + SUM + AVG + MAX + MIN)
-- Business Question: Give a complete performance summary per product.
-- Clauses Used: SELECT, COUNT, SUM, AVG, MAX, MIN, ROUND, GROUP BY
-- ============================================================

SELECT  Product,
        COUNT(*) AS Total_Orders,
        ROUND(SUM(TotalPrice), 2) AS Total_Revenue,
        ROUND(AVG(TotalPrice), 2) AS Avg_Order_Value,
        ROUND(MAX(TotalPrice), 2) AS Highest_Order,
        ROUND(MIN(TotalPrice), 2) AS Lowest_Order
FROM    orders
GROUP BY Product
ORDER BY Total_Revenue DESC;

-- ============================================================
-- QUERY 09 | DATE FUNCTION (Monthly Trend)
-- Business Question: What is the monthly revenue trend?
-- Clauses Used: SELECT, strftime(), COUNT, SUM, AVG, GROUP BY
-- ============================================================

SELECT  strftime('%Y-%m', Date) AS Month,
        COUNT(*) AS Total_Orders,
        ROUND(SUM(TotalPrice), 2) AS Monthly_Revenue,
        ROUND(AVG(TotalPrice), 2) AS Avg_Order_Value
FROM    orders
GROUP BY Month
ORDER BY Month;

-- ============================================================
-- QUERY 10 | SUBQUERY (Revenue % Share)
-- Business Question: What percentage of total revenue does each product contribute?
-- Clauses Used: SELECT, SUM, ROUND, Subquery in SELECT, GROUP BY
-- ============================================================

SELECT  Product,
        COUNT(*) AS Total_Orders,
        ROUND(SUM(TotalPrice), 2) AS Total_Revenue,
        ROUND(
            SUM(TotalPrice) * 100.0 /
            (SELECT SUM(TotalPrice) FROM orders),
        2) AS Revenue_Share_Pct
FROM    orders
GROUP BY Product
ORDER BY Total_Revenue DESC;

-- ============================================================
-- END OF SCRIPT | DecodeLabs Project 3 | SQL Data Analysis
-- ============================================================
