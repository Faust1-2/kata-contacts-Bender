# run time python3 contacts.py <number> && rm ./contacts.sqlite3 with different numbers 
# and save the real time into a list in a file

numbers=(10 100 500 1000 5000 10000 50000 100000 1000000 10000000 100000000)

output_file="timings.txt"

# empty the output file
> "$output_file"

for number in "${numbers[@]}"; do
    # Use the time command and extract the real time
    { time python3 contacts.py "$number" && rm ./contacts.sqlite3 ; } 2>&1 | grep real | awk '{print $2}' >> "$output_file"
done
