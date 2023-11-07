from subprocess import run
import json
from datetime import datetime
from time import sleep
import re


def execute(command):
    return run(command.split(), capture_output=True).stdout.decode("utf-8")

def json_response(command):
    return json.loads(execute(command))

def aws_get_time(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')

def get_container(profile, service, region='us-west-2'):
    command = f"aws lightsail get-container-images --region {region} --profile {profile} --service-name {service}"
    response = json_response(command)
    return [{'name':i.get('image'),'date':aws_get_time(i.get('createdAt'))} for i in response.get('containerImages')]

def push_image(profile, service, image, label, region='us-west-2'):
    command = f"aws lightsail push-container-image --region {region} --profile {profile} --service-name {service} --image {image} --label {label}"
    run(command.split(), capture_output=True).stdout.decode("utf-8")

def create_container(profile, service, region='us-west-2'):
    command = f"aws lightsail create-container-service-deployment --profile {profile} --region {region} --service-name {service} --containers file://containers.json --public-endpoint file://public-endpoint.json"
    run(command.split(), capture_output=True).stdout.decode("utf-8")

def build(image):
    command = f"docker build -t {image} ."
    image_id = get_docker_image(image)
    while (img_id := get_docker_image(image)) == image_id:
        try:
            execute(command)
        except Exception as e:
            print(e)
            execute(command)
        sleep(5)
        

def get_newest_container(data):
    newest_date = max([i.get('date') for i in data])
    return [i.get('name') for i in data if i.get('date') == newest_date][0]

def containers(data, container):
    writeout = {
        f"{container}": {
            "image": f"{get_newest_container(data)}",
            "ports": {
                "5000": "HTTP"
            }
        }
    }
    with open('containers.json','w') as file:
        file.writelines(json.dumps(writeout))
        file.close()
    
def end_point(image):
    writeout = {
        "containerName": f"{image}",
        "containerPort": 5000
    }
    with open('public-endpoint.json','w') as file:
        file.writelines(json.dumps(writeout))
        file.close()

def get_input():
    try:
        output = input('Input label, Q for quit: ')
        if output == 'Q':
            quit()
        return output
    except:
        get_input()

def get_docker_image(image):
    command = "docker image ls"
    data = execute(command)
    data = data.replace('IMAGE ID','IMAGE_ID')
    data = data.split('\n')
    headers = data[0].split()
    data = data[1:-1]
    data = [{headers[0]:i[0],headers[1]:i[1],headers[2]:i[2],headers[3]:i[3],headers[4]:i[4]} for i in [re.split(r'\s{2,}',d) for d in data]]
    response = [i.get('IMAGE_ID') for i in data if i.get('REPOSITORY') == image and i.get('TAG') == 'latest'][0]
    return response
    

if __name__ == "__main__":
    docker = 'posweb'
    service = 'pos'
    container = 'pos'
    label = docker+get_input()
    profile = 'pos-test'
    #build(docker)
    push_image(profile, service, docker+':latest', label)
    data = get_container(profile, service)
    containers(data, container)
    end_point(docker)
    create_container(profile, service)