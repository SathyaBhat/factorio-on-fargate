### Factorio on Fargate

A headless [Factorio](https://factorio.com/) server running on [AWS Fargate](https://aws.amazon.com/fargate/), with EFS backed storage. Provisioned using CDK.

### Getting started

- [Install CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
- `pip install -r requirements.txt` to install required libraries
- Run `cdk synth` to preview the CloudFormation template that will be generated
- Run `cdk deploy` to deploy the infra

### Todo

- [ ] Make a service
- [ ] Add logging config
- [ ] Setup auto scaling to scale-in when CPU drops to low (ex, when disconnected)
- [ ] Factorio server config, save creation/load
- [ ] How to start again?
