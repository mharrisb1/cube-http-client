-- Create accounts table
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create opportunities table
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    account_id INTEGER REFERENCES accounts(id),
    amount DECIMAL(10, 2),
    stage VARCHAR(255),
    close_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create contacts table
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    account_id INTEGER REFERENCES accounts(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create leads table
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    company VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create cases table
CREATE TABLE cases (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id),
    contact_id INTEGER REFERENCES contacts(id),
    subject VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    priority VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP
);

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    priority VARCHAR(50),
    due_date TIMESTAMP,
    completed_date TIMESTAMP,
    related_to_id INTEGER,
    related_to_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create campaigns table
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    start_date DATE,
    end_date DATE,
    budgeted_cost DECIMAL(10, 2),
    actual_cost DECIMAL(10, 2),
    expected_revenue DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create price_books table
CREATE TABLE price_books (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create opportunity_line_items table
CREATE TABLE opportunity_line_items (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert mock data into accounts table
INSERT INTO accounts (name, industry)
VALUES 
    ('Acme Corporation', 'Technology'),
    ('Globex Corporation', 'Finance'),
    ('Soylent Corp', 'Manufacturing'),
    ('Initech', 'Software'),
    ('Umbrella Corp', 'Pharmaceuticals'),
    ('Wayne Enterprises', 'Technology'),
    ('Stark Industries', 'Defense'),
    ('Oscorp', 'Biotechnology'),
    ('Wonka Industries', 'Food & Beverage'),
    ('Tyrell Corporation', 'Technology');

-- Insert mock data into opportunities table
INSERT INTO opportunities (name, account_id, amount, stage, close_date)
VALUES 
    ('Opportunity 1', 1, 50000, 'Prospecting', '2024-09-01'),
    ('Opportunity 2', 2, 200000, 'Negotiation', '2024-10-15'),
    ('Opportunity 3', 3, 120000, 'Closed Won', '2024-08-22'),
    ('Opportunity 4', 4, 75000, 'Proposal', '2024-11-05'),
    ('Opportunity 5', 5, 150000, 'Qualification', '2024-12-12'),
    ('Opportunity 6', 6, 300000, 'Prospecting', '2024-09-15'),
    ('Opportunity 7', 7, 500000, 'Negotiation', '2024-10-20'),
    ('Opportunity 8', 8, 250000, 'Closed Lost', '2024-08-30'),
    ('Opportunity 9', 9, 100000, 'Proposal', '2024-11-10'),
    ('Opportunity 10', 10, 600000, 'Qualification', '2024-12-20');

-- Insert mock data into contacts table
INSERT INTO contacts (first_name, last_name, email, phone, account_id)
VALUES 
    ('John', 'Doe', 'john.doe@acme.com', '555-1234', 1),
    ('Jane', 'Smith', 'jane.smith@globex.com', '555-5678', 2),
    ('Bill', 'Jones', 'bill.jones@soylent.com', '555-8765', 3),
    ('Susan', 'Brown', 'susan.brown@initech.com', '555-4321', 4),
    ('Alice', 'Johnson', 'alice.johnson@umbrella.com', '555-0000', 5),
    ('Bruce', 'Wayne', 'bruce.wayne@wayneenterprises.com', '555-1111', 6),
    ('Tony', 'Stark', 'tony.stark@starkindustries.com', '555-2222', 7),
    ('Norman', 'Osborn', 'norman.osborn@oscorp.com', '555-3333', 8),
    ('Willy', 'Wonka', 'willy.wonka@wonkaindustries.com', '555-4444', 9),
    ('Eldon', 'Tyrell', 'eldon.tyrell@tyrellcorporation.com', '555-5555', 10);

-- Insert mock data into leads table
INSERT INTO leads (first_name, last_name, email, phone, company, status)
VALUES 
    ('Michael', 'Scott', 'michael.scott@dundermifflin.com', '555-0101', 'Dunder Mifflin', 'New'),
    ('Pam', 'Beesly', 'pam.beesly@dundermifflin.com', '555-0202', 'Dunder Mifflin', 'Contacted'),
    ('Jim', 'Halpert', 'jim.halpert@dundermifflin.com', '555-0303', 'Dunder Mifflin', 'Qualified'),
    ('Dwight', 'Schrute', 'dwight.schrute@dundermifflin.com', '555-0404', 'Dunder Mifflin', 'Converted'),
    ('Stanley', 'Hudson', 'stanley.hudson@dundermifflin.com', '555-0505', 'Dunder Mifflin', 'Unqualified'),
    ('Clark', 'Kent', 'clark.kent@dailyplanet.com', '555-0606', 'Daily Planet', 'New'),
    ('Peter', 'Parker', 'peter.parker@bugle.com', '555-0707', 'Daily Bugle', 'Contacted'),
    ('Bruce', 'Banner', 'bruce.banner@greenlabs.com', '555-0808', 'Gamma Labs', 'Qualified'),
    ('Diana', 'Prince', 'diana.prince@themyscira.com', '555-0909', 'Themyscira', 'Converted'),
    ('Steve', 'Rogers', 'steve.rogers@shield.com', '555-1001', 'SHIELD', 'Unqualified');

-- Insert mock data into users table
INSERT INTO users (username, password, email, role)
VALUES 
    ('admin', 'adminpassword', 'admin@example.com', 'Admin'),
    ('jdoe', 'password123', 'john.doe@example.com', 'Sales'),
    ('jsmith', 'password456', 'jane.smith@example.com', 'Marketing'),
    ('bjones', 'password789', 'bill.jones@example.com', 'Support'),
    ('susanbrown', 'password321', 'susan.brown@example.com', 'Sales'),
    ('bwayne', 'darkknight', 'bruce.wayne@wayneenterprises.com', 'CEO'),
    ('tstark', 'ironman', 'tony.stark@starkindustries.com', 'CTO'),
    ('nosborn', 'greengoblin', 'norman.osborn@oscorp.com', 'CEO'),
    ('wwonka', 'chocolate', 'willy.wonka@wonkaindustries.com', 'Founder'),
    ('etyrell', 'replicant', 'eldon.tyrell@tyrellcorporation.com', 'CEO');

-- Insert mock data into cases table
INSERT INTO cases (account_id, contact_id, subject, status, priority, description, created_at, closed_at)
VALUES
(1, 1, 'Login Issue', 'Closed', 'High', 'User cannot login to the portal.', '2024-08-01', '2024-08-02'),
(2, 2, 'Billing Error', 'Open', 'Medium', 'Customer reported incorrect billing.', '2024-08-03', NULL),
(3, 3, 'Feature Request', 'Closed', 'Low', 'Request for new feature in the product.', '2024-08-04', '2024-08-06'),
(4, 4, 'Product Defect', 'Open', 'High', 'Reported issue with the product.', '2024-08-05', NULL),
(5, 5, 'Account Suspension', 'Closed', 'High', 'Account suspended without notice.', '2024-08-07', '2024-08-08');

-- Insert mock data into tasks table
INSERT INTO tasks (subject, status, priority, due_date, completed_date, related_to_id, related_to_type, created_at)
VALUES
('Follow up on lead', 'Completed', 'High', '2024-08-01', '2024-08-02', 1, 'lead', '2024-07-30'),
('Send proposal to customer', 'Pending', 'Medium', '2024-08-10', NULL, 1, 'opportunity', '2024-08-05'),
('Call customer support', 'Completed', 'Low', '2024-08-01', '2024-08-01', 1, 'case', '2024-07-31'),
('Prepare presentation for client', 'In Progress', 'High', '2024-08-15', NULL, 1, 'account', '2024-08-10'),
('Review product feedback', 'Pending', 'Medium', '2024-08-20', NULL, 1, 'case', '2024-08-18');

-- Insert mock data into campaigns table
INSERT INTO campaigns (name, status, start_date, end_date, budgeted_cost, actual_cost, expected_revenue, created_at)
VALUES
('Summer Promo', 'Active', '2024-06-01', '2024-08-31', 10000, 8500, 50000, '2024-05-15'),
('Winter Discount', 'Planned', '2024-12-01', '2025-01-31', 15000, 0, 75000, '2024-10-01'),
('New Product Launch', 'Completed', '2024-01-01', '2024-03-31', 20000, 21000, 100000, '2023-12-01'),
('Referral Program', 'Active', '2024-07-01', '2024-12-31', 5000, 2500, 25000, '2024-06-15'),
('Flash Sale', 'Completed', '2024-05-01', '2024-05-07', 3000, 2800, 15000, '2024-04-20');

-- Insert mock data into products table
INSERT INTO products (name, description, price, created_at)
VALUES
('Product A', 'Description of Product A', 100.00, '2024-01-01'),
('Product B', 'Description of Product B', 200.00, '2024-02-01'),
('Product C', 'Description of Product C', 300.00, '2024-03-01'),
('Product D', 'Description of Product D', 400.00, '2024-04-01'),
('Product E', 'Description of Product E', 500.00, '2024-05-01');

-- Insert mock data into price_books table
INSERT INTO price_books (name, description, created_at)
VALUES
('Standard Price Book', 'Default price book for all products.', '2024-01-01'),
('Discount Price Book', 'Price book for discount campaigns.', '2024-06-01');

-- Insert mock data into opportunity_line_items table
INSERT INTO opportunity_line_items (opportunity_id, product_id, quantity, price, total_price, created_at)
VALUES
(1, 1, 10, 100.00, 1000.00, '2024-08-01'),
(2, 2, 5, 200.00, 1000.00, '2024-08-02'),
(3, 3, 3, 300.00, 900.00, '2024-08-03'),
(4, 4, 2, 400.00, 800.00, '2024-08-04'),
(5, 5, 1, 500.00, 500.00, '2024-08-05');
