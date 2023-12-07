#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_indexer_info

short_description: Get information about Radarr indexer.

version_added: "1.0.0"

description: Get information about Radarr indexer.

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
# Gather information about all indexers.
- name: Gather information about all indexers
  devopsarr.radarr.radarr_indexer_info:

# Gather information about a single indexer.
- name: Gather information about a single indexer
  devopsarr.radarr.radarr_indexer_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
indexers:
    description: A list of indexers.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: indexer ID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
        enable_automatic_search:
            description: Enable automatic search flag.
            returned: always
            type: bool
            sample: true
        enable_interactive_search:
            description: Enable interactive search flag.
            returned: always
            type: bool
            sample: false
        enable_rss:
            description: Enable RSS flag.
            returned: always
            type: bool
            sample: true
        priority:
            description: Priority.
            returned: always
            type: int
            sample: 1
        download_client_id:
            description: Download client ID.
            returned: always
            type: int
            sample: 0
        config_contract:
            description: Config contract.
            returned: always
            type: str
            sample: "BroadcastheNetSettings"
        implementation:
            description: Implementation.
            returned: always
            type: str
            sample: "BroadcastheNet"
        protocol:
            description: Protocol.
            returned: always
            type: str
            sample: "torrent"
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
        fields:
            description: field list.
            type: list
            returned: always
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


def list_indexers(result):
    try:
        return client.list_indexer()
    except Exception as e:
        module.fail_json('Error listing indexers: %s' % to_native(e.reason), **result)


def populate_indexers(result):
    indexers = []
    # Check if a resource is present already.
    for indexer in list_indexers(result):
        if module.params['name']:
            if indexer['name'] == module.params['name']:
                indexers = [indexer.dict(by_alias=False)]
        else:
            indexers.append(indexer.dict(by_alias=False))
    return indexers


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.IndexerApi(module.api)
    result = dict(
        changed=False,
        indexers=[],
    )

    # List resources.
    result.update(indexers=populate_indexers(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
