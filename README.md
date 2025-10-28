# MopBot
A Discord bot for configiuring permissions declaratively in YAML.

## Features
- Declarative configuration for role permissions
- Support for mapping the same config across multiple guilds, such as a staging server

## To-Do
- `--check` flag to only run the config schema check.
- Configuring channel and category permissions.

## Usage
### Environment Variables
- `BOT_TOKEN`: Required, a bot token for the Discord API
- `ENV`: A non-production environment to use, as specified in the config file. If not set, uses the `production` environment.

### Config File
See the [example config file](/config.yaml) and the [JSON Schema](/src/mopbot/data/schema.json).

### Using a different environment
To run config for a non-production environment, set the environment variable `ENV` to the key from your configuration file.