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
<!--- Begin command usage -->
```
```
<!--- End command usage -->

## Configuration
Mopbot is configured via a YAML configuration file, the full format for which is defined via [a JSON-Schema](/src/mopbot/data/schema.json). The default configuration target is `config.yaml`, but this can be changed by passing a different file name or path as a command-line argument (eqivilent to the `config_file` input on GitHub Actions).

### Environments
To make it so one configuration can be applied to muliple guilds (for example, a production server and a testing server), Mopbot uses arbitrary configuration IDs to refer to roles internally. Configuration IDs can be any string.

At runtime, configuration IDs are mapped to Discord role IDs via environment definitions, set under the top-level `environments:` key in the config file. Each environment definition must contain a `guild_id:` key containing the target Discord server ID and a `roles:` key, containing key-value pairs of configuration IDs and their corresponding Discord role IDs.

The default environment is called `production`. Other environments can be chosen by setting the `ENV` environment variable.

```yaml example.yml
environments:
  production:
    guild_id: <discord_id>
    roles:
      role_configuration_id_1: <discord_id>
      role_configuration_id_2: <discord_id>
  staging:
    guild_id: <discord_id>
    roles:
      role_configuration_id_1: <discord_id>
      role_configuration_id_2: <discord_id>
```

### Roles
Roles are applied through an array of definitions under the top-level `roles:` key.

Each definition must include an array `roles:` containing configuration IDs for each role it targets. 

```yml
roles:
  - roles: 
    - role_configuration_id_1
    - role_configuration_id_2
    #[role options and perms...]
```

Role definitions apply cumulatively from top to bottom, so a config file can apply general permissions and options to a group of roles in one definition, then apply additional permissions and options to a subset of those roles in a later definition.

```yml
roles:
  - roles: 
    - role_configuration_id_1
    - role_configuration_id_2
    #<role options and perms...>
  
  - roles:
    - role_configuration_id_2
    #<additional role options and perms...>
```

#### Role Options
Mopbot supports setting the certain role options as top-level keys within a definition.

```yml
roles:
  - roles: 
    - role_configuration_id_1
    - role_configuration_id_2
    name: Pretty Role
    color: "#88001b"
    hoist: false
    mentionable: false
```

**Default Behavior:** If an option is not set explicitly by any definition, Mopbot will not modify that option.

**Duplicate Behavior:** If multiple definitions set the same option for a role, Mopbot will log a warning. Where there is a conflict, the state set by the bottom-most definition applies.

The following role options are supported:
- `name: (string)` is the role's new display name.
- `color: (string)` is a 6-character hexidecimal string representing an RGB color (RRGGBB) to apply to the role. A leading `#` is permitted but not required.
- `hoist: (bool)` determines whether the role should be displayed separately on the Discord UI sidebar.
- `mentionable: (bool)` determines whether the role can be metioned by users who do not have the `mention_everyone` permission.

#### Permissions
Mopbot supports setting permission nodes under the top-level `perms:` key within a definition.

```yml
roles:
  - roles:
    - role_configuration_id_1
    perms:
      read_messages: true
      send_messages: true
```

**Default Behavior:** Permission nodes that are not set explicitly by any definition will be set to false.

**Duplicate Behavior:** If multiple definitions set the same permission node for a role, Mopbot will log a warning. Where there is a conflict, the state set by bottom-most definition applies.

The following permission nodes are supported:
- `add_reactions`
-  `administrator`
-  `attach_files`
-  `ban_members`
-  `change_nickname`
-  `connect`
-  `create_events`
-  `create_expressions`
-  `create_instant_invite`
-  `create_polls`
-  `create_private_threads`
-  `create_public_threads`
-  `deafen_members`
-  `embed_links`
-  `external_emojis`
-  `external_stickers`
-  `kick_members`
-  `manage_channels`
-  `manage_emojis`
-  `manage_emojis_and_stickers`
-  `manage_events`
-  `manage_expressions`
-  `manage_guild`
-  `manage_messages`
-  `manage_nicknames`
-  `manage_permissions`
-  `manage_roles`
-  `manage_threads`
-  `manage_webhooks`
-  `mention_everyone`
-  `moderate_members`
-  `move_members`
-  `mute_members`
-  `pin_messages`
-  `priority_speaker`
-  `read_message_history`
-  `read_messages`
-  `request_to_speak`
-  `send_messages`
-  `send_messages_in_threads`
-  `send_polls`
-  `send_tts_messages`
-  `send_voice_messages`
-  `set_voice_channel_status`
-  `speak`
-  `stream`
-  `use_application_commands`
-  `use_embedded_activities`
-  `use_external_apps`
-  `use_external_emojis`
-  `use_external_sounds`
-  `use_external_stickers`
-  `use_soundboard`
-  `use_voice_activation`
-  `view_audit_log`
-  `view_channel`
-  `view_creator_monetization_analytics`
-  `view_guild_insights`
