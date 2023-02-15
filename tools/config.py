import yaml

# Load YML Configurations
yml_configs = {}
with open('config.yml', 'r') as config:
    yml_configs = yaml.safe_load(config)