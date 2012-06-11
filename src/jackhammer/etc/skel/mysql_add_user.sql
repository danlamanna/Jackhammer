#############
# Grant a priviledge to the user which will create the user if it doesn't exists,  so that
# DROP USER won't throw an error if the user does NOT exists.
#############

GRANT USAGE ON *.* TO '%USERNAME%'@'localhost';
DROP USER '%USERNAME%'@'localhost';
GRANT USAGE ON *.* TO '%USERNAME%'@'%';
DROP USER '%USERNAME%'@'%';

#############
# CREATE THE USER AND GRAND PRIVILEGES
#############

CREATE USER '%USERNAME%'@'localhost';
CREATE USER '%USERNAME%'@'%';
SET PASSWORD FOR '%USERNAME%'@'localhost' = PASSWORD('%USERPASS%');
SET PASSWORD FOR '%USERNAME%'@'%' = PASSWORD('%USERPASS%');

GRANT ALL PRIVILEGES ON *.* TO '%USERNAME%'@'localhost' WITH GRANT OPTION; 
GRANT ALL PRIVILEGES ON *.* TO '%USERNAME%'@'%' WITH GRANT OPTION;
