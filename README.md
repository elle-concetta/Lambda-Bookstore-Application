# Lambda Bookstore Application
This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- bookstore - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

PyCharm AWS Toolkit with SAM CLI to build and deploy serverless Bookstore application.

* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)

### Demo Video
[![Lambda Bookstore Application Demo]          // Title
(https://i.ytimg.com/vi/Hc79sDi3f0U/maxresdefault.jpg)] // Thumbnail
([https://www.youtube.com/watch?v=Hc79sDi3f0U](https://www.youtube.com/watch?v=z6kZF5Nx5v4) "Lambda Bookstore Application Demo")    // Video Link



## Deploy Bookstore Application
The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need to install the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.

Find API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally
Build your application with the `sam build --use-container` command.

```bash
BooksFunction$ sam build --use-container
```
The SAM CLI installs dependencies defined in `bookstore/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        BookstoreCreatePostAPI:
          Type: Api
          Properties:
            Path: '/user'
            Method: POST
```

## Run and Validate Application APIs
In the top menu on PyCharm, click on `Run` and then `Edit Configurations`:

Create book with POST API method:
```console
{
"body": "{\"book_id\": \"4444\",\"isbn\": \"1256478967009\",\"title\": \"Where the Crawdads Sing\",\"author\": \"David Cook\",\"publisher\": \"Penguin Books\",...}"
}
```
Get top 10 bestsellers with GET API method:
```console
{
 "pathParameters": {
    "title": ""
}
}
```
Get books by genre with GET API method:
```console
{
 "pathParameters": {
    "genre": "Biography"
}
}
```
Get books by rating with GET API method:
```console
{
 "pathParameters": {
    "rating": "4"
}
}
```
Delete book details with DELETE API method:
```console
{
 "pathParameters": {
    "Id": ""
}
}
```
Update price of books under publisher by discount with PUT API method:
```console
 {
  "body": "{\"price\": \"23.99\", \"discount\": \"15\"}",
  "pathParameters": {
    "publisher": "Jiangsu Literature"
}
}
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests
Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
BooksFunction$ pip install -r tests/requirements.txt --user
# unit test
BooksFunction$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
BooksFunction$ AWS_SAM_STACK_NAME="booksfunction" python -m pytest tests/integration -v
```

## Resources
See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.
