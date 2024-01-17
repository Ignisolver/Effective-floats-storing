In this benchmark compares storages of json with data in:
- json
- bson
- bson with only values
- binary (packed with python struct module)
- and compressed all above
To run benchmark navigate in your shell to 'structures_benchmark folder and run:
```shell
pip install -r requirements.txt
python structures_benchmark.py
```
You cen edit 'TEST_FILE_NAME' and 'BENCHMARK_NAME' variables on the top of structures_benchmark.py.  
Then in folder results/<BENCHMARK_NAME> you will see REPORT.txt file which contains the results. 

ValuesExtractor in utils.py class implements extracting values (list of doubles) from json.