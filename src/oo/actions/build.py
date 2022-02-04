from ast import arg
from distutils.command.build import build
import sys
import os
import re
from oo.config import main_config, root_dir

__docker_make_path__ = f"{root_dir}/DockerMake.yml"

def docker_make(docker_make_target, **kwargs):

    docker_cmd = f'docker-make {docker_make_target} '

    if 'tag' in kwargs:
            docker_cmd += f"--tag {kwargs['tag']} "

    docker_cmd += f" -f {__docker_make_path__} "
    if 'repo' in kwargs:
        docker_cmd += f"--repository {kwargs['repo']} " 
    
    if 'build_args' in kwargs:
        for arg in kwargs['build_args']:
            key,value = arg
            docker_cmd += f"--build-arg {key}={value} "
    
    print(docker_cmd)
    os.system(docker_cmd)

__common_build_args__ = [
    ("db_user", os.environ['OO_DB_USER']),
    ("db_pwd", os.environ['OO_DB_PWD'])
]

def build_docker_image():
    build_args = []
    build_args.extend(__common_build_args__)

    if sys.argv[3] == 'nse-update':
        
        docker_make('nse-update', 
            tag =  main_config["app_version"],
            repo = main_config["app_name"],
            build_args = build_args
        )
        

def process():
    if sys.argv[2] == 'image':
        build_docker_image()
