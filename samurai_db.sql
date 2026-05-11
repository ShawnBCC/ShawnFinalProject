CREATE DATABASE samurai_db;
USE samurai_db;

CREATE TABLE samurai_figures (
    figure_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    clan VARCHAR(100) NOT NULL,
    material VARCHAR(100) NOT NULL,
    height_cm DECIMAL(5,2) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    quantity INT NOT NULL,
    description TEXT,
    image_file VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO samurai_figures (name, clan, material, height_cm, price, quantity, description, image_file)
VALUES
('Takeda Shingen', 'Takeda Clan', 'Metal, Plastic', 21.00, 45.00, 3, 'Miniature samurai figure with armor', 'samurai1.jpg'),
('Naoe Kanetsugu', 'Naoe Clan', 'Metal, Plastic', 21.00, 45.00, 2, 'Detailed miniature warrior', 'samurai2.jpg'),
('Ishida Mitsunari', 'Ishida Clan', 'Metal, Plastic', 21.00, 45.00, 4, 'Purple armor collectible', 'samurai3.jpg'),
('Kuroda Yoshitaka', 'Kuroda Clan', 'Metal, Plastic', 21.00, 45.00, 1, 'Historical samurai miniature', 'samurai4.jpg'),
('Imagawa Yoshimoto', 'Imagawa Clan', 'Metal, Plastic', 21.00, 45.00, 5, 'Red and gold armor figure', 'samurai5.jpg'),
('Maeda Keiji', 'Maeda Clan', 'Metal, Plastic', 21.00, 45.00, 3, 'Unique armor display', 'samurai6.jpg');