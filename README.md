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

| Name              |                         Description                          | Type | AllowedValues/Pattern | Default |
| :---------------: | :----------------------------------------------------------: | :--: | :--------------------------: | :-----: |
| AcmCertificateArn | The Amazon Resource Name (ARN) of an AWS Certificate Manager (ACM) for your domain name certificate. |  String    |  N/A                            |      N/A   |
|   DomainName                |       The DNS name of the website, such as example.com.                     | String     |       N/A                       |    N/A     |
|        ErrorResponse           |        Single-page applications can handle their own error responses. Single-page returns 403 and 404 errors to /index.html as a 200 response, seperate points those files to /403.html and /404.html respectively, none does not handle 403 and 404 errors.                                                      |  String    |                single-page, seperate, none              |      N/A   |
|            HostedZoneId       |        The ID of the Hosted Zone of the domain name.                                                      |    AWS::Route53::HostedZone::Id  |               N/A               |      N/A   |
|       LoggingBucket            |        Name of the logging bucket where CloudFront and S3  will reside. If a logging bucket is not specified, logging will be disabled.                                                      |   String   |           N/A                   |         |
|      LoggingPrefix             |       An optional string to prefix the log filenames in the logging bucket. S3/ or CloudFront/ will automatically prefix the log filenames, for example S3 bucket  will prefixed as YourPrefix/S3/.                                                       |    String  |          .*\/$                    |     /    |
|      StoreCache             |      Set to false to not store cache.                                                        |    String  |         true, false                     |     true    |
|       UploadWebsiteSource            |        The custom resource will fail to upload if the website source is too big. Set this to false to disable it.                                                      |    String  |                true, false              |      true   |
|       UseCustomDomain            |         If there is a custom domain being used with this set, set to true.                                                     |   String   |          true, false                  |     true    |
|       UseHttpSecurityHeaders            |        HTTP security headers mitigate attacks and harden against security vulnerabilities. Tailor the function in functions/security-headers/ to the needs of the website for full protection.                                                      |  String    |              true, false                |     true    |
|        UseIndexHtmlOnDeepLinks           |      Some static site generators always use index.html on the end of their deep links. Using this Lambda edge function example.com/foo/index.html will become example.com/foo/.                                                        |    String  |          true, false                    |     false    |
|     UseRoute53ForDNS              |    If using a DNS service other than Route 53, set to false.                                                          |   String   | true, false                             |  true     |

### Deployment

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
