
import toml

with open('config.toml') as config_file:
    config = toml.load(config_file)