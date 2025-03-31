# library-book-auto-renewer
A program to automatically renew my library books.

## Package Lambda Function
```commandline
cd /lambda
```
#### Install dependencies into a package folder
```commandline
pip install -r requirements.txt -t package/
```

#### Move your lambda entry point inside the package
```
cp main.py package/
```

#### Copy the app directory inside the package
```commandline
cp -r ../app package/
```

#### Zip the package for AWS Lambda
```commandline
cd package
zip -r ../lambda_function.zip .
```