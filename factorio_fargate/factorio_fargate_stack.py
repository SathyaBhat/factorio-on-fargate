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
