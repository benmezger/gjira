#!/usr/bin/env python3

import pathlib
from typing import Callable

from jinja2 import Environment, Template, meta


def get_template_lines(path: str = None) -> Template:
    if path is None:
        path = str(pathlib.Path(".").joinpath(".commit.template"))
    with open(path) as f:
        for line in f:
            yield line


def get_template_context(
    path: str = None, replace: Callable = lambda x: x.replace("__", ".")
) -> list:

    env = Environment()
    context = []
    for line in get_template_lines(path):
        ast = env.parse(line)
        context.extend(meta.find_undeclared_variables(ast))

    # This is needed because find_undeclared_variables cannot find find
    # inner variables
    return [replace(i) for i in context]


def generate_template(context: dict, path):
    with open(path) as f:
        return Template(f.read()).render(**context)
