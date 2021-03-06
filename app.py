#!/usr/bin/env python3

from aws_cdk import core

from factorio_fargate.factorio_fargate_stack import FactorioFargateStack


app = core.App()
FactorioFargateStack(app,
                    "factorio-fargate",
                    env=core.Environment(region="eu-west-1"))

app.synth()
