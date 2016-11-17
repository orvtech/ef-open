# noinspection PyClassHasNoInit

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

from ef_utils import env_valid, get_account_alias, get_env_short, global_env_valid, whereami

class EFContext(object):
  """
  Class holds environment/account-related context for tools and resolvers
  and helps assure consistency in, for example, trimming "env" to "env_short"
  """

  def __init__(self):
    # service environment
    self._account_alias = None
    self._env = None # prod, staging, proto<n>, global -- the name used in AWS
    self._env_short = None # prod, staging, proto, global -- the generic name for matching when templating
    # _env_full deals with naming differences for "proto<n>" and "global.<alias>" in the service registry
    self._env_full = None # prod, staging, proto, global.<account_alias> -- name found in SR
    self._service = None
    self._service_registry_file = None

    # tool context
    self._commit = None
    self._devel = None
    self._verbose = None
    self._whereami = whereami()

  @property
  def account_alias(self):
    """The account alias in use"""
    return self._account_alias

  @property
  def env(self):
    """Full name of the environment, e.g. 'prod' or 'proto3'"""
    return self._env

  @env.setter
  def env(self, value):
    """
    Sets context.env, context.env_short, and context.account_alias if env is valid
    For envs of the form "global.<account>" and "mgmt.<account_alias>",
    env is captured as "global" or "mgmt" and account_alias is parsed out of the full env rather than looked up
    Args:
      value: the fully-qualified env value
    Raises:
      ValueError if env is not valid
    """
    env_valid(value)
    self._env_full = value
    if value.find(".") == -1:
      # plain environment, e.g. prod, staging, proto<n>
      self._env = value
      self._account_alias = get_account_alias(value)
    else:
      # "<env>.<account_alias>" form, e.g. global.ellationeng or mgmt.ellationeng
      self._env, self._account_alias = value.split(".")
      # since we extracted an env, must reconfirm that it's legit
      global_env_valid(self._env)
    self._env_short = get_env_short(value)

  @property
  def env_short(self):
    """Short (generic) name of the environment, e.g. 'prod' or 'proto' or 'global'"""
    return self._env_short

  @property
  def env_full(self):
    """Name of the environment as expected in the service registry, e.g. 'prod' or 'proto' or 'global.ellationeng'"""
    return self._env_full

  @property
  def service(self):
    """A single service's service object from service registry"""
    return self._service

  @service.setter
  def service(self, value):
    self._service = value

  @property
  def service_registry_file(self):
    """Full path to the service_registry_file"""
    return self._service_registry_file

  @service_registry_file.setter
  def service_registry_file(self, value):
    """
    Sets service registry path in context, doesn't check it
    Args:
      value: /path/to/service_registry_file.json
    """
    if type(value) is not str:
      raise TypeError("service_registry_file value must be str")
    self._service_registry_file = value

  @property
  def commit(self):
    """True if the tool should actually execute changes"""
    return self._commit

  @commit.setter
  def commit(self, value):
    if type(value) is not bool:
      raise TypeError("commit value must be bool")
    self._commit = value

  @property
  def devel(self):
    """True if the tool should allow devel exceptions"""
    return self._devel

  @devel.setter
  def devel(self, value):
    if type(value) is not bool:
      raise TypeError("devel value must be bool")
    self._devel = value

  @property
  def verbose(self):
    """True if the tool should print extra info"""
    return self._verbose

  @verbose.setter
  def verbose(self, value):
    if type(value) is not bool:
      raise TypeError("verbose value must be bool")
    self._verbose = value

  @property
  def whereami(self):
    """Hosted ec2? lambda? local vm?"""
    return self._whereami
