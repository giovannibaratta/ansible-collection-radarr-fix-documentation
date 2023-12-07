#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_quality_profile_info

short_description: Get information about Radarr quality profile.

version_added: "1.0.0"

description: Get information about Radarr quality profile.

options:
    name:
        description: Name.
        type: str

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all quality profiles.
- name: Gather information about all quality profiles
  devopsarr.radarr.radarr_quality_profile_info:

# Gather information about a single quality profile.
- name: Gather information about a single quality profile
  devopsarr.radarr.radarr_quality_profile_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
quality_profiles:
    description: A list of quality profiles.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Quality Profile ID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: Example
        upgrade_allowed:
            description: Upgrade allowed flag.
            returned: always
            type: bool
            sample: false
        cutoff:
            description: Quality ID to which cutoff.
            returned: always
            type: int
            sample: 1
        cutoff_format_score:
            description: Cutoff format score.
            returned: always
            type: int
            sample: 0
        min_format_score:
            description: Min format score.
            returned: always
            type: int
            sample: 0
        language:
            description: Language.
            returned: always
            type: dict
            sample:
                name: Any
                id: -1
        quality_groups:
            description: Quality groups
            returned: always
            type: list
            elements: dict
            sample: []
        formats:
            description: Format items list.
            returned: always
            type: list
            elements: dict
            sample: []
'''

from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_module import RadarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str'),
    )


def list_quality_profile(result):
    try:
        return client.list_quality_profile()
    except Exception as e:
        module.fail_json('Error listing quality profiles: %s' % to_native(e.reason), **result)


def populate_quality_profiles(result):
    profiles = []
    # Check if a resource is present already.
    for profile in list_quality_profile(result):
        if module.params['name']:
            if profile['name'] == module.params['name']:
                profiles = [profile.dict(by_alias=False)]
        else:
            profiles.append(profile.dict(by_alias=False))
    return profiles


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.QualityProfileApi(module.api)
    result = dict(
        changed=False,
        quality_profiles=[],
    )

    # List resources.
    result.update(quality_profiles=populate_quality_profiles(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
