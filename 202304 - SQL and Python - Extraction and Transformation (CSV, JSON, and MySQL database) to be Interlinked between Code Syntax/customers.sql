USE tugas1;
CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(100),
  phone VARCHAR(15)
);

INSERT INTO customers (customer_id, first_name, last_name, email, phone)
VALUES (1, 'John', 'Doe', 'john.doe@example.com', '+1-123-456-7890'),
       (2, 'Jane', 'Smith', 'jane.smith@example.com', '+1-098-765-4321'),
       (3, 'Alice', 'Johnson', 'alice.johnson@example.com', '+1-555-123-4567'),
       (4, 'Bob', 'Brown', 'bob.brown@example.com', '+1-555-987-6543'),
       (5, 'Charlie', 'Davis', 'charlie.davis@example.com', '+1-555-333-2222'),
       (6, 'Eva', 'Garcia', 'eva.garcia@example.com', '+1-555-444-1111'),
       (7, 'Frank', 'Harris', 'frank.harris@example.com', '+1-555-555-5555'),
       (8, 'Grace', 'Clark', 'grace.clark@example.com', '+1-555-666-7777'),
       (9, 'Henry', 'Lewis', 'henry.lewis@example.com', '+1-555-888-9999'),
       (10, 'Ivy', 'Walker', 'ivy.walker@example.com', '+1-555-111-2222'),
       (11, 'Jack', 'Hall', 'jack.hall@example.com', '+1-555-333-4444');

SELECT * FROM customers;