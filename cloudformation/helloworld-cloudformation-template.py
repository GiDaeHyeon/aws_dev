from troposphere import Template, Parameter, ec2, Base64, Join, Ref, Output, GetAtt######################################### Variables########################################ApplicationPort = "3000"KeyName = 'NGINX't = Template()t.description = "Effective DevOps in AWS: HelloWorld web Application"######################################### Parameters"""Parameter Object는 식별자, 설명, 매개변수, 제약조건설명 등을 인자로 받는다."""########################################t.add_parameter(    Parameter(        'KeyPair',        Description='Name of an existing EC2 KeyPair to SSH',        Type=f'AWS::EC2::KeyPair::{KeyName}',        ConstraintDescription='must be the name of an existing EC2 KeyPair'    ))######################################### Resources########################################## SecurityGroupt.add_resource(    ec2.SecurityGroup(        'SecurityGroup',        GroupDescription=f'Allow SSH and TCP/{ApplicationPort} access',        SecurityGroupIngress=[            ec2.SecurityGroupRule(                IpProtocol='tcp',                FromPort='22',                ToPort='22',                CidrIp='0.0.0.0/0'            ),            ec2.SecurityGroupRule(                IpProtocol='tcp',                FromPort=ApplicationPort,                ToPort=ApplicationPort,                CidrIp='0.0.0.0/0'            )        ]    ))## Instancesud = Base64(    Join(        '\n',        ['#!/bin/bash',         'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash', #바보등신! * 2         '. ~/.nvm/nvm.sh',         'nvm install node',         'wget https://bit.ly/2vESNuc -O /home/ec2-user/helloworld.js',         'nohup node /home/ec2-user/helloworld.js &']    ))t.add_resource(    ec2.Instance(        'instance',        ImageId='ami-08c64544f5cfcddd0',        InstanceType='t2.micro',        SecurityGroups=[Ref('SecurityGroup')],        KeyName=Ref('KeyPair'),        UserData=ud    ))######################################### Outputs########################################t.add_output(    Output(        'InstancePublicIP',        Description='public IP of our Instance',        Value=GetAtt('instance', 'PublicIp')    ))t.add_output(    Output(        'WebUrl',        Description='Application endpoint',        Value=Join(            '',            [                'http://', GetAtt('instance', 'PublicDnsName'), ':', ApplicationPort            ]        )    ))print(t.to_json())