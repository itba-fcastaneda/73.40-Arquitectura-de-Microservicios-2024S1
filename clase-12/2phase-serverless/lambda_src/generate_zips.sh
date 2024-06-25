
directories=("P1" "P2" "orders")

for dir in "${directories[@]}"; do

    cd "$dir"

    rm ./*.zip

    for file in "."/*.py; do
        filename=$(basename "$file" .py)
        cp "$file" "./lambda_function.py"
        zip -r "./$filename.zip" "lambda_function.py"
        rm lambda_function.py
    done

    cd ..
done

cd ./utils_layer

zip -r "./python.zip" ./python/*

cd ..
