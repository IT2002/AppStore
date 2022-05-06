# Construct the URI from the .env
DB_HOST='localhost'
DB_NAME='prosgres'
DB_USER='postgrs'
DB_PORT='5432'
DB_PASSWORD='baboon13'

while IFS= read -r line
do
  if [[ $line == DB_HOST* ]]
  then
    DB_HOST=$(cut -d "=" -f2- <<< $line | tr -d \')
  elif [[ $line == DB_NAME* ]]
  then
    DB_NAME=$(cut -d "=" -f2- <<< $line | tr -d \' )
  elif [[ $line == DB_USER* ]]
  then
    DB_USER=$(cut -d "=" -f2- <<< $line | tr -d \' )
  elif [[ $line == DB_PORT* ]]
  then
    DB_PORT=$(cut -d "=" -f2- <<< $line | tr -d \')
  elif [[ $line == DB_PASSWORD* ]]
  then
    DB_PASSWORD=$(cut -d "=" -f2- <<< $line | tr -d \')
  fi
done < ".env"

URI="postgres://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"

# Run the scripts to insert data.
psql ${URI} -f sql/AppStoreClean.sql
psql ${URI} -f sql/AppStoreSchema.sql
psql ${URI} -f sql/AppStoreCustomers.sql
psql ${URI} -f sql/AppStoreGames.sql
psql ${URI} -f sql/AppStoreDownloads.sql
psql ${URI} -f sql/PetsittingSchema.sql
psql ${URI} -f sql/Petsittingjoboffer.sql
psql ${URI} -f sql/Petsittingpending.sql
psql ${URI} -f sql/Petsittingpet.sql
psql ${URI} -f sql/Petsittingportfolio.sql
psql ${URI} -f sql/Petsittingtransaction.sql