To run benchmark navigate in your shell to 'Effective-floats-storing' folder and run:
```shell
pip install -r requirements.txt
python structures_benchmark.py
```
You cen edit 'TEST_FILE_NAME' and 'BENCHMARK_NAME' variables on the top of structures_benchmark.py.  
Then in folder <BENCHMARK_NAME> you will see REPORT.txt file which contains the results.  
To test decompression time navigate in your shell to "app" folder and run:
```shell
npm install express
npm install multer
node app.js
```
Then open your browser and go to "http://localhost:3000/" url.  
Select the file you want to decompress and click 'Extract' button  
Then in your shell you will se decompression time.