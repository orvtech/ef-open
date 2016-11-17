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

class EFConfig:
  """
  Installation-specific and global settings shared by all EF tools
  """

  #### Customizable params ####
  # Region to work in when no region is otherwise specified (tools only support 1 region at present - this one)
  DEFAULT_REGION = "us-west-2"
  # Repo where tools and all EF data are
  EF_REPO = "github.com/##PATH/TO/REPO##"
  EF_REPO_BRANCH = "master"
  # Map environment::account alias (aliases must profiles in .aws/credentials for local use)
  ENV_ACCOUNT_MAP = {
    "prod": "##ALIAS_OF_PROD_ACCOUNT##",
    "proto": "##ALIAS_OF_PROTO_ACCOUNT##",
    "staging": "##ALIAS_OF_STAGING_ACCOUNT##"
  }
  # Number of prototype environments, numbered 0..N-1
  PROTO_ENVS = 4
  # Bucket where late-bound service configs are found
  S3_CONFIG_BUCKET = "##PREFIX##-global-configs"


  #### Derived/generated config constants ####
  LOCAL_VM_LABEL = "localvm"
  PARAMETER_FILE_SUFFIX = ".parameters.json"
  POLICY_TEMPLATE_PATH_SUFFIX = "/policy_templates/"
  VALID_ENV_REGEX = "prod|staging|proto[0-{}]|global|mgmt".format(PROTO_ENVS - 1)

  # Convenient list of all mapped accounts
  ACCOUNT_LIST = set(ENV_ACCOUNT_MAP.values())

  # Convenient list of all possible valid environments
  ENV_LIST = ["prod", "staging"]
  ENV_LIST.extend(map(lambda x: "global." + x, ACCOUNT_LIST))
  ENV_LIST.extend(map(lambda x: "mgmt." + x, ACCOUNT_LIST))
  ENV_LIST.extend(map(lambda x: "proto" + str(x), range(PROTO_ENVS)))
  ENV_LIST = sorted(ENV_LIST)

  # These environments are for account-wide resources; they have a ".<ACCOUNT_ALIAS>" suffix
  ACCOUNT_SCOPED_ENVS = ["global", "mgmt"]
