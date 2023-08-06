locust --master &
timeout 20 sh -c 'until nc -z localhost $0; do sleep 1; done' 8089
for i in {1..3}
do
    locust --worker &
done


