"""
A library containing functions for generating lists of important modules.
These are mostly used in decode.py and in unit tests
"""

import os
import pkg_resources
from glob import iglob

from dshell.util import get_plugin_path

#def get_plugins(plugin_path, logger=None):
def get_plugins(logger=None):
    """
    Generate a list of all available plugin modules, either in the
    dshell.plugins directory or external packages
    """
    plugins = {}
    # List of directories above the plugins directory that we don't care about
    import_base = get_plugin_path().split(os.path.sep)[:-1]

    # Walk through the plugin path and find any Python modules that aren't
    # __init__.py. These are assumed to be plugin modules and will be
    # treated as such.
    for root, dirs, files in os.walk(get_plugin_path()):
        if '__init__.py' in files:
            import_path = root.split(os.path.sep)[len(import_base):]
            for f in iglob("{}/*.py".format(root)):
                name = os.path.splitext(os.path.basename(f))[0]
                if name != '__init__':
                    if name in plugins and logger:
                        logger.warning("Duplicate plugin name found: {}".format(name))
                    module = '.'.join(["dshell"] + import_path + [name])
                    plugins[name] = module

    # Next, try to discover additional plugins installed externally.
    # Uses entry points in setup.py files.
    for ep_plugin in pkg_resources.iter_entry_points("dshell_plugins"):
        if ep_plugin.name in plugins and logger:
            logger.warning("Duplicate plugin name found: {}".format(name))
        plugins[ep_plugin.name] = ep_plugin.module_name

    return plugins

def get_output_modules(output_module_path, logger=None):
    """
    Generate a list of all available output modules under an output_module_path
    """
    modules = []
    for f in iglob("{}/*.py".format(output_module_path)):
        name = os.path.splitext(os.path.basename(f))[0]
        if name != '__init__' and name != 'output':
            # Ignore __init__ and the base output.py module
            modules.append(name)
    return modules
