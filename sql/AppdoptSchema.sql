CREATE TABLE IF NOT EXISTS users(
	first_name VARCHAR(64) NOT NULL,
	last_name VARCHAR(64) NOT NULL,
	email VARCHAR(128) UNIQUE NOT NULL,
	username VARCHAR(50) UNIQUE NOT NULL,
	phone_number VARCHAR(16) PRIMARY KEY,
	password VARCHAR(50) NOT NULL
);
	
CREATE TABLE IF NOT EXISTS posts(
	post_id INTEGER PRIMARY KEY,
	username VARCHAR(50) REFERENCES users(username),
	pet VARCHAR(20) NOT NULL,
	breed VARCHAR(64) NOT NULL,
	date_of_post DATE NOT NULL,
	age_of_pet VARCHAR(16),
	price NUMERIC (10,2) NOT NULL CHECK(price >= 0),
	description VARCHAR(1200),
	title VARCHAR(128) NOT NULL,
	status VARCHAR(50) DEFAULT 'AVAILABLE',
	phone_number VARCHAR(16),
	FOREIGN KEY (phone_number) REFERENCES users(phone_number) ON DELETE CASCADE ON UPDATE CASCADE
	);
  
CREATE TABLE transactions(
	post_id INTEGER,
	date_of_sale DATE NOT NULL,
	seller_phone_number VARCHAR(16) REFERENCES users(phone_number),
	buyer_phone_number VARCHAR(16) REFERENCES users(phone_number),
	FOREIGN KEY (post_id) REFERENCES posts(post_id)
);
