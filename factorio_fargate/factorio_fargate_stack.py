from attr import validate
from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_efs as efs
import aws_cdk.aws_ecs as ecs


class FactorioFargateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        volume_name = 'factorio'
        self.vpc = ec2.Vpc(self,
                            "vpc",
                            max_azs=1,
                            nat_gateways=0)
        
        self.efs_fs = efs.FileSystem(self, 'Filesystem', vpc=self.vpc, enable_automatic_backups=True)
        self.ecs = ecs.Cluster(self, "Fargate", vpc=self.vpc )
        self.task_definition = ecs.FargateTaskDefinition(self, 
                                                        "Factorio",
                                                        cpu=2048,
                                                        memory_limit_mib=4096,
                                                        volumes=[
                                                            ecs.Volume(
                                                                name=volume_name,
                                                                efs_volume_configuration=ecs.EfsVolumeConfiguration(file_system_id=self.efs_fs.file_system_id)
                                                                )
                                                            ]
                                                        )
        self.container = self.task_definition.add_container("hello-world",
                                            image=ecs.ContainerImage.from_registry(name="hello-world"))
        self.container.add_mount_points(ecs.MountPoint(container_path="/factorio",
                                                       read_only=False,
                                                       source_volume= volume_name))
        udp_34197_mapping= ecs.PortMapping(container_port=34197,
                                            host_port=34197, 
                                            protocol=ecs.Protocol.UDP)

        tcp_27015_mapping= ecs.PortMapping(container_port=27015,
                                            host_port=27015,
                                            protocol=ecs.Protocol.TCP)
        self.container.add_port_mappings(udp_34197_mapping, tcp_27015_mapping)
                                         
        core.CfnOutput(self, "VPC",
                        value=self.vpc.vpc_id)
        core.CfnOutput(self, "EFS",
                        value=self.efs_fs.file_system_id)
        core.CfnOutput(self, "TaskDef",
                        value=self.task_definition.task_definition_arn)    
        core.CfnOutput(self, "Container",
                        value=self.container.container_name)