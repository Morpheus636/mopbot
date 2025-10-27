import yaml

config = []

# Load configuration file from disk.
with open("config.yaml") as stream:
    config = yaml.safe_load(stream);


def validate(config):
    # Guild ID is required
    assert type(config.get("guild_id")) is int

    # ROLES MODULE
    roles = config.get("roles")
    if roles is not None:
        # Top level item under roles should be a list.
        assert type(roles) is list
        for i in roles:
            # Each item under roles should be a dictionary.
            assert type(i) is dict

            # The dictionary should contain two lists.
            role_ids = i["role_ids"]
            perms = i["permissions"]
            assert type(role_ids) is list
            assert type(perms) is dict

            # Each item in the role_ids list should be an int.
            for j in role_ids:
                assert type(j) is int
    
            # Each pair in the perms list should be a pair of str, bool
            for j in perms:
                assert type(j) is str
                assert type(perms[j]) is bool