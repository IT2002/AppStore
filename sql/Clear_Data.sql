/*******************

  Cleaning script

*******************/
DROP TRIGGER IF EXISTS Update_Listing ON GPU_Listing;
DROP FUNCTION IF EXISTS Log_Listing();
DROP VIEW IF EXISTS all_listing1;
DROP TABLE IF EXISTS Rental;
DROP TABLE IF EXISTS GPU_Listing_Archive;
DROP TABLE IF EXISTS GPU_Listing;
DROP TABLE IF EXISTS GPU;
DROP TABLE IF EXISTS User1;
