# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False

from ansible.module_utils.basic import AnsibleModule, env_fallback


class RadarrModule(AnsibleModule):
    def __init__(self, argument_spec, bypass_checks=False, no_log=False,
                 mutually_exclusive=None, required_together=None,
                 required_one_of=None, add_file_common_args=False,
                 supports_check_mode=False, required_if=None):

        argument_spec = self._merge_dictionaries(
            argument_spec,
            dict(
                radarr_url=dict(
                    required=True,
                    type='str',
                    fallback=(env_fallback, ['RADARR_URL'])),
                radarr_api_key=dict(
                    required=True,
                    type='str',
                    fallback=(env_fallback, ['RADARR_API_KEY']),
                    no_log=True)
            )
        )

        # manage python 2 with except
        try:
            super().__init__(
                argument_spec,
                bypass_checks=bypass_checks,
                no_log=no_log,
                mutually_exclusive=mutually_exclusive,
                required_together=required_together,
                required_one_of=required_one_of,
                add_file_common_args=add_file_common_args,
                supports_check_mode=supports_check_mode,
                required_if=required_if,
            )
        except TypeError:
            super(RadarrModule, self).__init__(
                argument_spec,
                bypass_checks=bypass_checks,
                no_log=no_log,
                mutually_exclusive=mutually_exclusive,
                required_together=required_together,
                required_one_of=required_one_of,
                add_file_common_args=add_file_common_args,
                supports_check_mode=supports_check_mode,
                required_if=required_if,
            )

        self._validate()

        configuration = radarr.Configuration(
            host=self.params["radarr_url"]
        )
        configuration.api_key['X-Api-Key'] = self.params["radarr_api_key"]
        self.api = radarr.ApiClient(configuration)

    def _validate(self):
        if not HAS_RADARR_LIBRARY:
            self.fail_json(msg="Please install the radarr library")

    def _merge_dictionaries(self, a, b):
        new = a.copy()
        new.update(b)
        return new
