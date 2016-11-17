"""
Copyright 2016 Ellation, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
from os.path import isfile

from ef_config import EFConfig

class EFServiceRegistry(object):
  """
  Wraps interactions with the Service Registry
  """

  def __init__(self, service_registry_file):
    """
    Args:
      service_registry_file - the file containing the service registry
    """
    if not isfile(service_registry_file):
      raise IOError("Not a file: {}".format(service_registry_file))

    service_registry_fh = open(service_registry_file, "r")
    self.service_registry_json = json.load(service_registry_fh)

    if not self.service_registry_json.has_key("services"):
      raise RuntimeError("service registry file doesn't have a 'services' section")

  def services(self):
    return self.service_registry_json["services"]

  def iter_services(self):
    return self.service_registry_json["services"].iteritems()


  def get_valid_envs_for_service(self, service_name):
    """
    Args:
      service_name: the name of the service in the service registry
    Returns:
      a list of strings - all valid environments for 'service'
    Raises:
      ValueError if the service wasn't found
    """
    if not self.services().has_key(service_name):
      raise RuntimeError("service registry doesn't have service: {}".format(service_name))
    service_record = self.services()[service_name]

    # Return empty list if service has no "environments" section
    if not (service_record.has_key("environments")):
      return []
    # Otherwise gather up the envs
    service_record_envs = service_record["environments"]
    result = []
    for e in service_record_envs:
      if "proto" == e:
        result.extend(map(lambda x: "proto" + str(x), range(EFConfig.PROTO_ENVS)))
      else:
        result.append(e)
    return result

  def get_service(self, service_name):
    """
    Args:
      service_name: the name of the service in the service registry
    Returns:
      the entire service record from the service registry
    Raises:
      ValueError if the service wasn't found
    """
    if not self.services().has_key(service_name):
      raise RuntimeError("service registry doesn't have service: {}".format(service_name))
    return self.services()[service_name]
