
import json
import logging
import os

from jsonpath_rw import parse

PREFIX_USER_PROVIDED = "user-provided"
PREFIX_CLOUD_FOUNDRY = "cloudfoundry"
PREFIX_ENV_VAR = "env"
PREFIX_FILE = "file"

logger = logging.getLogger("ibmcloudenv")

loadedMappings = {}

def setLogLevel(level):
    '''
    Set log level to CRITICAL, ERROR, WARNING, INFO, DEBUG, or NOTSET
    set to WARNING by default.
    '''
    logger.setLevel(level)

def strip_leading_slash(path):
    if path and (path[0] == "/" or path[0] == "\\"):
        return path[1:]
    return path

def get_service_cred_by_name(name, artifact):
    if (not artifact) or (not name):
        logger.debug("got blank jsonpath or artifact")
        return ""
    for service_name, service_value in artifact.items():
        if isinstance(service_value, list) and len(service_value) > 0:
            for instance in service_value:
                if instance["name"] == name:
                    return instance["credentials"]
    return ""

def parse_json_path(jsonpath, artifact, service_name=None, credential=None):
    '''
    Looks through artifact for match for jsonpath; returns what is found or {}
    '''
    logger.debug("parsing " +jsonpath)
    if (not artifact) or (not jsonpath):
        logger.debug("got blank jsonpath or artifact")
        return ""

    # tree = objectpath.Tree(artifact)
    # value = tree.execute(jsonpath)
    # # value_array = list(ids)
    expr = parse(jsonpath)
    value_array = [match.value for match in expr.find(artifact)]
    if value_array:
        value = value_array[0]
        if type(value == "string"):
            logger.debug(value)
            return value
        else:
            logger.debug(json.dumps(value))
            return json.dumps(value)
    else:
        logger.debug("couldn't find jsonpath " + jsonpath + " in artifact")
    return ""

def value_from_cloud_foundry(line):
    '''
    Get value from VCAP_SERVICES or VCAP_APPLICATION
    '''
    vcap, services, application = {}, {}, {}
    if "VCAP_SERVICES" in os.environ:
        try:
            services = json.loads(os.environ["VCAP_SERVICES"])
        except ValueError:
            pass
    if "VCAP_APPLICATION" in os.environ:
        try:
            application = json.loads(os.environ["VCAP_APPLICATION"])
        except ValueError:
            pass
    vcap = services.copy()
    vcap.update(application)

    json_search_path = line[1]
    if line[1][0] != "$":
        # json_search_path = '$..[@.name is "' + line[1] + '"].credentials'
        return get_service_cred_by_name(json_search_path, vcap)
    else:
        return parse_json_path(json_search_path, vcap)

def value_from_user_provided(line):
    '''
    Get value from user_provided in VCAP_SERVICES 
    '''
    vcap, services, application, credential_value = {}, {}, {}, None
    if "VCAP_SERVICES" in os.environ:
        try:
            services = json.loads(os.environ["VCAP_SERVICES"])
        except ValueError:
            pass

    if len(line) == 3:
        vcap = services.copy()

        # user-provided:service-name1ae34:credkey
        service_info_name = line[1]
        credential_key = line[2]
        json_search_path = "$..{}".format(credential_key)
        
        expr = parse(json_search_path)
        if not PREFIX_USER_PROVIDED in vcap:
            logger.debug("Couldn't credential in find user-provided search pattern")
            return ""

        cred_array = vcap[PREFIX_USER_PROVIDED]

        for value in cred_array:
            if "name" in value and value["name"] == service_info_name:
                value_array = [match.value for match in expr.find(value["credentials"])]
                credential_value = value_array[0] if len(value_array) > 0 else credential_value
                logger.debug(credential_value)
                return credential_value

    logger.debug("couldn't find jsonpath " + json_search_path + " in artifact")
    return "" 

def value_from_env_var(line):
    '''
    Get value from environment variable
    '''
    if line[1] in os.environ:
        env_value = os.environ[line[1]]
        if len(line) == 3:
            try:
                env_data = json.loads(env_value)
                return parse_json_path(line[2], env_data)
            except ValueError:
                return ""
        else:
            return env_value
    else:
        logger.debug("Environment variable " + line[1] + " not found.")
    return ""

def value_from_file(line):
    '''
    Get credential value from provided file
    '''
    line[1] = strip_leading_slash(line[1])
    abs_path_to_file = os.path.abspath(line[1])
    if os.path.isfile(abs_path_to_file):
        cred_data = open(line[1]).read()
        if len(line) >= 3:
            file_data = json.loads(cred_data)
            return parse_json_path(line[2], file_data)
        else:
            return cred_data
    else:
        logger.debug("couldn't find " + abs_path_to_file)
    return ""

def parse_search_patterns(entry):
    '''
    Loops through the search patterns for an entry, and returns a /
    value for the entry based on the first working search pattern /
    (or "" if none work)
    '''
    value = {}
    gen = entry["searchPatterns"]
    for line in gen:
        logger.debug("search pattern line: " +line)
        line_pieces = line.split(":")

        if line_pieces[0] == PREFIX_USER_PROVIDED:
            value = value_from_user_provided(line_pieces)
        elif line_pieces[0] == PREFIX_CLOUD_FOUNDRY:
            value = value_from_cloud_foundry(line_pieces)
        elif line_pieces[0] == PREFIX_ENV_VAR:
            value = value_from_env_var(line_pieces)
        elif line_pieces[0] == PREFIX_FILE:
            value = value_from_file(line_pieces)
        else:
            logger.warn("Unknown searchPattern prefix %s Supported prefixes: user-provided, cloudfoundry, env, file", line_pieces[0]);
        # Stop parsing if value has been found
        if value:
            break
    return value

def parse_pattern_file(config_data):
    '''
    Resolve all values for parsing file
    '''
    for key, value in config_data.items():
        logger.debug(key)
        if "searchPatterns" in value and len(value["searchPatterns"]) > 0:
            entry = parse_search_patterns(value)
            if not entry:
                logger.warn("No value found for " + key)
            if type(entry) == dict:
                entry = json.dumps(entry)
            loadedMappings[key] = entry

def parse_pattern_file_v2(config_data):
    '''
        Resolve all values for parsing file
    '''
    for service_key in config_data.keys():
        logger.debug('serviceKey ' + service_key)
        for credential_key in config_data[service_key].keys():
            logger.debug('credentialKey ' + credential_key)
            service_search_patterns = config_data[service_key][credential_key]
            if "searchPatterns" in service_search_patterns and len(service_search_patterns['searchPatterns']) > 0:
                entry = parse_search_patterns(service_search_patterns)
                if not entry:
                    logger.warn("No value found for " + service_key)
                if type(entry) == dict:
                    entry = str(json.dumps(entry))
                if not service_key in loadedMappings:
                    loadedMappings[service_key] = {}
                loadedMappings[service_key][credential_key] = entry

def init(new_config_file="server/config/mappings.json"):
    '''
    Use custom file path, and set up file.
    '''
    new_config_file = strip_leading_slash(new_config_file)
    config_file = os.path.abspath(new_config_file)
    if (not os.path.isfile(config_file)):
        logger.warning("The specified config.json file %s does not exist", config_file)
        return
    raw_config = open(config_file).read()
    config_data = json.loads(raw_config)
    version = None
    if 'version' in config_data:
        version = config_data['version']
        del config_data['version']

    if version and version == 1:
        parse_pattern_file(config_data)
    elif version and version == 2:
        parse_pattern_file_v2(config_data)
    else:
        parse_pattern_file(config_data)

def getDictionary(key):
    '''
    Return a dictionary for the key value provided
    '''
    logger.debug("Looking for " + key)
    try:
        logger.debug("Found " + str(loadedMappings[key]))
        return json.loads(str(loadedMappings[key]))
    except ValueError:
        logger.debug("Found " + str(loadedMappings[key]))
        if type(loadedMappings[key]) == dict:
            return loadedMappings[key]
        return {"value": loadedMappings[key]}
    except KeyError:
        return {}

def getString(key):
    '''
    Return a stringified dictionary for the key value provided
    '''
    logger.debug("Looking for " +key)
    logger.debug("Found " + loadedMappings[key])
    return loadedMappings[key]
