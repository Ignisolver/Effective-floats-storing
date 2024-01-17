This package provides some utilities for **yaptide** "https://github.com/yaptide" app.  
  
The problem was efficient transfer and storage of json files which contained a lot of floating-point numbers.    
"Raw" json format was inefficient because it can use more than 20 bytes to store single 8-bytes double number.   
  
In **structures_benchmark package** You can find benchmark, and a way to convert original json to more efficient format.  
In **optimal_transfer** package You can find a ready implementation of sending zip file via http requests and recreating original json from this more efficient structure.
  
To see the details please read the README.md file in specific package