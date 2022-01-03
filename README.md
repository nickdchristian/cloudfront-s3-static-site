# cloudfront-s3-static-site
Creates a CloudFront distribution with an S3 origin to host a static website.

## Getting Started

### Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/)
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

[Use AWS CLI to configure your AWS credentials](https://docs.aws.amazon.com/cli/latest/reference/configure/). This CloudFormation template must be deployed in us-east-1 due to CloudFront and Lambda Edge.

```bash
aws configure
```

Once configured, install SAM CLI in order to deploy the CloudFormation template.

### Parameters

| Name                    | Description                                                  | AllowedValues/Pattern                           | Default        |
| ----------------------- | ------------------------------------------------------------ | ----------------------------------------------- | -------------- |
| AcmCertificateArn       | The Amazon Resource Name (ARN) of an AWS Certificate Manager (ACM) for your domain name certificate. | N/A                                             | N/A            |
| ArchitectureType        | Single Page Applications (SPA) can handle their own error responses, as well as default to index.html the end of every path. Legacy has its own error response pages, assumed here to be 404.html and 4.3.html. | spa, legacy, none | spa
| DomainName              | The DNS name of the website, such as example.com.            | N/A                                             | N/A            |
| HostedZoneId            | The ID of the Hosted Zone of the domain name.                | N/A                                             | N/A            |
| LoggingBucket           | Name of the logging bucket where CloudFront and S3  will reside. If a logging bucket is not specified, logging will be disabled. | N/A                                             |                |
| LoggingPrefix           | An optional string to prefix the log filenames in the logging bucket. S3/ or CloudFront/ will automatically prefix the log filenames, for example S3 bucket  will prefixed as YourPrefix/S3/. | .*\/$                                           | /              |
| PriceClass              | The price class for the CloudFront distribution determines what edge locations are utilized and costs. Go to https://aws.amazon.com/cloudfront/pricing/ to learn more about price classes and other CloudFront costs. | PriceClass_100, PriceClass_200, PriceClass_ All | PriceClass_all |
| RedirectFunctionality   | If set to true this redirects all requests from the www subdomain to the base domain. Must have both domains in your ACM certificate. Addtional redirect functionality can be added or changed in the RedirectFunction resource. | true, false | true
| StoreCache              | Set to false to not store cache.                             | true, false                                     | true           |
| UploadWebsiteSource     | The custom resource will fail to upload if the website source is too big. Set this to false to disable it. | true, false                                     | true           |
| UseCustomDomain         | If there is a custom domain being used with this set, set to true. | true, false                                     | true           |
| UseHttpCustomHeaders    | Adds several common HTTP security headers to the response from CloudFront. Other headers and CORS may be added to this function too. | true, false                                     | true           |
| UseRoute53ForDNS        | If using a DNS service other than Route 53, set to false.    | true, false                                     | true           |

### Additional Configuration

#### Custom Headers

Default behavior includes generic security headers. Please review and adapt them to your own needs. Additional headers and CORS support can be added too.
```yaml
  CustomResponseHeadersPolicy:
    Condition: UseCustomHeaders
    Properties:
      ResponseHeadersPolicyConfig:
        Name: !Sub '${AWS::StackName}-CustomHeadersPolicy'
        SecurityHeadersConfig:
          ContentSecurityPolicy:
            ContentSecurityPolicy: default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; frame-ancestors 'none'
            Override: true
          ContentTypeOptions:
            Override: true
          FrameOptions:
            FrameOption: DENY
            Override: true
          ReferrerPolicy:
            Override: true
            ReferrerPolicy: same-origin
          StrictTransportSecurity:
            AccessControlMaxAgeSec: !If
              - NoStoreCache
              - 0
              - 63072000
            IncludeSubdomains: true
            Override: true
            Preload: true
          XSSProtection:
            ModeBlock: true
            Override: true
            Protection: true
    Type: AWS::CloudFront::ResponseHeadersPolicy
```
More information:

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-responseheaderspolicy-responseheaderspolicyconfig.html

https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-response-headers-policies.html

 


#### Redirect behavior

By default, this redirects from www.example.com to example.com. This functionality can be modified and/or more redirection behaviors can be added to the function embedded in the template.

```yaml

 RedirectFunction:
    Condition: Redirect
    Properties:
      AutoPublish: true
      FunctionCode: |
        function handler(event) {
            var request = event.request;
            var host = request.headers.host.value;
            var uri = request.uri;
            var newurl = host.replace('www.','')

            if (host.startsWith('www.')) {
                    var response = {
                    statusCode: 302,
                        statusDescription: 'Found',
                    headers:
                            { "location": { "value": `https://${newurl}${uri}`} }
                    }

                    return response;
            }
            return request;
        }
      FunctionConfig:
        Comment: !Sub 'Handles all redirect logic'
        Runtime: cloudfront-js-1.0
      Name: !Sub '${AWS::StackName}-RedirectFunction'



```



#### Website source 
You will need to configure the relative path to the website source by looking for and editing the CodeUri path:

```yaml
SiteSource:
    Condition: UploadSiteSource
    Properties:
      AutoPublishAlias: live
      CodeUri: web-site/
      Handler: deployer.resource_handler
      Layers:
        - !GetAtt 'SiteDeploymentLayer.Outputs.Arn'
      Policies:
        - S3FullAccessPolicy:
            BucketName: !Ref 'WebsiteBucket'
      Runtime: python3.8
      Timeout: 600
    Type: AWS::Serverless::Function
```
### Deployment
In the same directory as template.yaml, it is recommended to run a guided deployment. This template will need the additonal capabilities of CAPABILITY_AUTO_EXPAND CAPABILITY_IAM.

```bash
sam deploy --guided --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM 
```

This command will prompt for all parameters.

After the first deployment, and if there are no parameter changes you no longer need to do a guided deployment.

```bash
sam deploy --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM 
```

You can view other values in the AWS CloudFormation console.

## Running tests

### cfn-lint

If you make changes to the template, it is recommended to run [cfn-lint](https://github.com/aws-cloudformation/cfn-python-lint) on the template to catch any obvious mistakes.

```bash
cfn-lint template.yaml
```

You can also validate with SAM.

```bash
sam validate
```

## License

This project is licensed under the APACHE LICENSE, VERSION 2.0.

## Acknowledgments

* [cloudformation-deploy-to-s3](https://github.com/serverlesspub/cloudformation-deploy-to-s3)