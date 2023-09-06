#from constructs import Construct
#from aws_cdk import (
#    Duration,
#    Stack,
#    aws_iam as iam,
#    aws_sqs as sqs,
#    aws_sns as sns,
#    aws_sns_subscriptions as subs,
#)


#class TestStack(Stack):

#    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#        super().__init__(scope, construct_id, **kwargs)

#        queue = sqs.Queue(
#            self, "TestQueue",
#            visibility_timeout=Duration.seconds(300),
#        )

#        topic = sns.Topic(
#            self, "TestTopic"
#        )

#        topic.add_subscription(subs.SqsSubscription(queue))

from constructs import Construct
#import aws_cdk as cdk

from aws_cdk import (
    Stack,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_ecs_patterns as ecs_patterns,
)
class TestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
 #       queue = sqs.Queue(
 #            self, "EcsCdkProjectQueue"	        #     visibility_timeout=Duration.seconds(300),
 #        )
	# Define the VPC
        vpc= ec2.Vpc(
	    self, "MyVpc",
	    max_azs=2,  # Set the desired number of Availability Zones
	    subnet_configuration=[
	        ec2.SubnetConfiguration(
	            name="Public",
	            subnet_type=ec2.SubnetType.PUBLIC,
	        ),
	        ec2.SubnetConfiguration(
	            name="Private",
	            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
        	),
	    ],
	)

	# Define the ECS Cluster for Flask
        flask_cluster= ecs.Cluster(
	    self, "FlaskCluster",
	    vpc=vpc,
	)

	# Define the ECS Cluster for Node.js
        nodejs_cluster= ecs.Cluster(
	    self,
	    "NodejsCluster",
	    vpc=vpc,
	)

	# Flask Task Definition
        flask_task_def= ecs.FargateTaskDefinition(
	    self,
	    "FlaskTaskDef",
	)
        flask_container= flask_task_def.add_container(
	    "FlaskContainer",
	    image=ecs.ContainerImage.from_registry("public.ecr.aws/j2w1f3l8/flask/flask:latest"),
	    memory_limit_mib=512,  # Adjust as needed
	    cpu=256  # Adjust as needed
	)

	# Node.js Task Definition
        nodejs_task_def= ecs.FargateTaskDefinition(
	    self,
	    "NodejsTaskDef",
	)
        nodejs_container= nodejs_task_def.add_container(
	    "NodejsContainer",
	    image=ecs.ContainerImage.from_registry("public.ecr.aws/j2w1f3l8/nodejs/nodejs:latest"),
	    memory_limit_mib=512,  # Adjust as needed
	    cpu=256  # Adjust as needed
	)


	
        # Create an ECS service for Node.js using Fargate
        ecs.FargateService(
            self, "NodejsService",
            cluster=nodejs_cluster,
            task_definition=nodejs_task_def,
            desired_count=2,  # Adjust as needed
        )

	# Create an ECS service for flask using Fargate
        ecs.FargateService(
            self, "FlaskService",
            cluster=flask_cluster,
            task_definition=flask_task_def,
            desired_count=2,  # Adjust as needed
        )

#        aws_cdk= ecs.FargateService(
#            self, "MyFargateService",
#            task_definition=flask_task_def,
#            cluster=nodejs_cluster,
#	)


	#Networking
#        flask_container.connections.allow_from(
#	    nodejs_cluster.connections,
#	    port_range=ec2.Port(
#	        protocol=ec2.Protocol.TCP,
#	        string_representation="FlaskAppPort",
#	        from_port=80,
#	        to_port=80
#	    ),
#	    description="Allow traffic from Node.js to Flask"
#	)

	#Load balancer
        alb= elbv2.ApplicationLoadBalancer(
	    self,
	    "NodejsALB",
	    vpc=vpc,
	    internet_facing=True,  # For public access
	)

	# Create a security group for ALB
        alb_security_group = ec2.SecurityGroup(
            self, "ALBSecurityGroup",
            vpc=vpc,
        )

	# Allow incoming traffic on ALB's listener port (e.g., 80)
        alb_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow incoming HTTP traffic",
        )

	# Create an ECS service

#                "container_name": "FlaskContainer",
#                "memory_limit_mib": 512,  # Adjust as needed
#                "cpu": 256,  # Adjust as needed
#            },
#            desired_count=2,  # Adjust as needed
#            listener_port=80,  # The port your application listens on
#            public_load_balancer=True,  # Use the ALB we created
#            security_groups=[alb_security_group],  # Attach ALB security group
#        )

# Define a listener for HTTP traffic
#        listener= alb.add_listener(
#	    "NodejsListener",
#	    port=80,
#	    open=True,
#	)

	# Create a target group for the Node.js ECS service
#        target_group= listener.add_targets(
#	    "NodejsTargetGroup",
#	    port=80,
#	    targets=[ecs.FargateService],
#	)

#app = cdk.App()
#app = core.App()
#TestStack(app, "test")
#EcsCdkProjectStack(app, "EcsCdkProjectStack")
#app.synth()
#app = cdk.App()
#EcsCdkProjectStack(app, "EcsCdkProjectStack")
#app.synth()
