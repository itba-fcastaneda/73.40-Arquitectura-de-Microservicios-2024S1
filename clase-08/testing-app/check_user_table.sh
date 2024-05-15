DB_HOST="$MYSQL_HOST"
DB_PORT="$MYSQL_PORT"
DB_USER="testing"
DB_PASS="testing"
DB_NAME="testing"

CHECK_TABLE_SQL="SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME' AND table_name='user';"

result=$(mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASS -D $DB_NAME -N -s -e "$CHECK_TABLE_SQL" 2>/dev/null)

if [ -n "$result" ] && [ "$result" -eq "1" ]; then
    echo "La tabla 'user' existe en la base de datos 'testing'."
    exit 0 
else
    echo "La tabla 'user' no existe en la base de datos 'testing'."
    exit 1
fi
