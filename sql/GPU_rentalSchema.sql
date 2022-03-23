/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS User1(
 First_name VARCHAR(64) NOT NULL,
 Last_name VARCHAR(64) NOT NULL,
 Email VARCHAR(64) UNIQUE NOT NULL,
 Customerid VARCHAR(16) PRIMARY KEY,
 Wallet_balance NUMERIC NOT NULL CHECK (wallet_balance >= 0),
 Phone_number NUMERIC NOT NULL,
 Pass_word VARCHAR(64) NOT NULL,
 Credit_card_number NUMERIC NOT NULL,
 Credit_card_type VARCHAR(64) NOT NULL);
	
 CREATE TABLE IF NOT EXISTS GPU(
 GPU_model VARCHAR(32),
 GPU_brand VARCHAR(32),
 PRIMARY KEY (GPU_model, GPU_brand),
 Memory_size VARCHAR(16) NOT NULL,
 Memory_type VARCHAR(16) NOT NULL,
 Memory_interface VARCHAR(16) NOT NULL,
 Base_clock VARCHAR(16) NOT NULL,
 Memory_clock VARCHAR(16) NOT NULL,
 Shaders NUMERIC NOT NULL,
 TMU NUMERIC NOT NULL,
 ROP NUMERIC NOT NULL
 );
  
 CREATE TABLE IF NOT EXISTS GPU_Listing(
 Listingid NUMERIC CHECK (Listingid >= 0) PRIMARY KEY,
 GPU_model VARCHAR(32),
 GPU_brand VARCHAR(32),
 FOREIGN KEY (GPU_model, GPU_brand) REFERENCES GPU(GPU_model, GPU_brand) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
 Customerid VARCHAR(16) REFERENCES User1(Customerid) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
 Available_start_day DATE NOT NULL,
 Available_end_day DATE NOT NULL,
 Price NUMERIC NOT NULL CHECK (Price >= 0));

 CREATE TABLE IF NOT EXISTS Rental(
 Borrower_id VARCHAR(16) REFERENCES User1(Customerid) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
 GPU_model VARCHAR(32),
 GPU_brand VARCHAR(32),
 FOREIGN KEY (GPU_model, GPU_brand) REFERENCES GPU(GPU_model, GPU_brand) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
 Listingid NUMERIC CHECK (Listingid >= 0) REFERENCES GPU_Listing(Listingid) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
 Start_day DATE NOT NULL,
 End_day DATE NOT NULL);
