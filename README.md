# MopBot
A Discord bot for configiuring permissions declaratively in YAML.

## Features
- Declarative configuration for role permissions
- Support for mapping the same config across multiple guilds, such as a staging server

## Usage
### Environment Variables
- `BOT_TOKEN`: Required, a bot token for the Discord API
- `ENV`: A non-production environment to use, as specified in the config file. If not set, uses the `production` environment.

### GitHub Actions
Mopbot includes a GitHub Action for use in a CI/CD deployment. Below is an example workflow.
```yml
name: Mopbot
on:
  push:
    branches: [ main ] 
jobs:
  mopbot:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Mopbot
        id: bot
        uses: "morpheus636/mopbot"
        with:
          config_file: config.yaml  # (Optional, config.yaml) Name of the config file relative to the project root
          check: false  # (Optional, false) Validate the config file against the schema but take no action
          dry_run: false  # (Optional, false) Run through the config file but do not apply the changes
        env:
          BOT_TOKEN: "${{ secrets.BOT_TOKEN }}"
          ENV: "production"
```

### Command-Line
See `mopbot --help` for information about command-line arguments.

### Config File
See the [example config file](/config.yaml) and the [JSON Schema](/src/mopbot/data/schema.json).