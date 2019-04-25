import shutil
import tempfile
import jinja2
import six
import datetime
import time
import os
from collections import defaultdict
from contextlib import contextmanager
import ruamel.yaml


@contextmanager
def tmp_directory():
    tmp_dir = tempfile.mkdtemp("_recipe")
    yield tmp_dir
    shutil.rmtree(tmp_dir)


class NullUndefined(jinja2.Undefined):
    def __unicode__(self):
        return self._undefined_name

    def __getattr__(self, name):
        return "{}.{}".format(self, name)

    def __getitem__(self, name):
        return '{}["{}"]'.format(self, name)


class MockOS(dict):
    def __init__(self):
        self.environ = defaultdict(lambda: "")
        self.sep = "/"


def render_meta_yaml(text):
    env = jinja2.Environment(undefined=NullUndefined)

    # stub out cb3 jinja2 functions - they are not important for linting
    #    if we don't stub them out, the ruamel.yaml load fails to interpret them
    #    we can't just use conda-build's api.render functionality, because it would apply selectors
    env.globals.update(
        dict(
            compiler=lambda x: x + "_compiler_stub",
            pin_subpackage=lambda *args, **kwargs: "subpackage_stub",
            pin_compatible=lambda *args, **kwargs: "compatible_pin_stub",
            cdt=lambda *args, **kwargs: "cdt_stub",
            load_file_regex=lambda *args, **kwargs: defaultdict(lambda: ""),
            datetime=datetime,
            time=time,
            target_platform="linux-64",
        )
    )
    mockos = MockOS()
    content = env.from_string(text).render(os=mockos, environ=mockos.environ)
    return content


@contextmanager
def update_conda_forge_config(feedstock_directory):
    """Utility method used to update conda forge configuration files

    Uage:
    >>> with update_conda_forge_config(somepath) as cfg:
    ...     cfg['foo'] = 'bar'
    """
    forge_yaml = os.path.join(feedstock_directory, "conda-forge.yml")
    if os.path.exists(forge_yaml):
        with open(forge_yaml, "r") as fh:
            code = ruamel.yaml.load(fh, ruamel.yaml.RoundTripLoader)
    else:
        code = {}

    # Code could come in as an empty list.
    if not code:
        code = {}

    yield code

    with open(forge_yaml, "w") as fh:
        fh.write(ruamel.yaml.dump(code, Dumper=ruamel.yaml.RoundTripDumper))
