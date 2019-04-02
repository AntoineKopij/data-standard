#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Beneficial Ownership Data Standard (alpha) documentation build configuration file
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import os
from recommonmark.transform import AutoStructify
from recommonmark.parser import CommonMarkParser

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinxcontrib.jsonschema','sphinxcontrib.opendataservices']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_parsers = {
    '.md': CommonMarkParser,
    }

source_suffix = ['.rst', '.md']

# The encoding of source files.
#
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Beneficial Ownership Data Standard'
copyright = '2017, OpenOwnership'
author = 'OpenOwnership'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.1'
# The full version, including alpha/beta/rc tags.
release = '0.1'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '_static/docson']

# The name of the Pygments (syntax highlighting) style to use.

import oods.pygments
oods.pygments.pygments_monkeypatch_style("oods", oods.pygments.OODSStyle)
pygments_style = 'oods'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
import oods.sphinxtheme
html_theme = 'sphinxtheme'
html_theme_path = [oods.sphinxtheme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'BODS'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None
locale_dirs = ['locale/', os.path.join(oods.sphinxtheme.get_html_theme_path(), 'locale')]
gettext_compact = False
gettext_uuid = True


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
     # The paper size ('letterpaper' or 'a4paper').
     #
     # 'papersize': 'letterpaper',

     # The font size ('10pt', '11pt' or '12pt').
     #
     # 'pointsize': '10pt',

     # Additional stuff for the LaTeX preamble.
     #
     # 'preamble': '',

     # Latex figure (float) alignment
     #
     # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'BeneficialOwnershipDataStandardalpha.tex', 'Beneficial Ownership Data Standard (alpha) Documentation',
     'OpenOwnership', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'beneficialownershipdatastandardalpha', 'Beneficial Ownership Data Standard (alpha) Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'BeneficialOwnershipDataStandardalpha', 'Beneficial Ownership Data Standard (alpha) Documentation',
     author, 'BeneficialOwnershipDataStandardalpha', 'One line description of project.',
     'Miscellaneous'),
]


# Adapted from https://github.com/OpenDataServices/sphinxcontrib-opendataservices/blob/master/sphinxcontrib/opendataservices.py#L50
# Should eventually move into there
import os
import json
from glob import glob
from collections import OrderedDict
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from jsonpointer import resolve_pointer
from pathlib import Path
from sphinx.directives.code import LiteralInclude

from bods_babel.translate import translate

class JSONValue(LiteralInclude):
    option_spec = {
        'pointer': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        dirname = os.path.dirname(env.doc2path(env.docname, base=None))
        relpath = os.path.join(dirname, self.arguments[0])
        abspath = os.path.join(env.srcdir, relpath)
        if not os.access(abspath, os.R_OK):
            raise self.warning('JSON file not readable: %s' %
                               self.arguments[0])

        with open(abspath) as fp:
            json_obj = json.load(fp, object_pairs_hook=OrderedDict)
        filename = str(self.arguments[0]).split("/")[-1].replace(".json", "")
        try:
            title = self.options['title']
        except KeyError as e:
            title = filename
        pointed = resolve_pointer(json_obj, self.options['pointer'])

        string = json.dumps(pointed, indent='    ')
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]
        return [nodes.paragraph(string,string)]


def translate_schema_and_codelists(language='en'):
    # The root of the repository.
    basedir = Path(os.path.realpath(__file__)).parents[1]
    build_dir = basedir / 'docs' / '_build' / 'html' / language
    static_dir = build_dir / '_static'

    localedir = basedir / 'docs' / 'locale'
    # The gettext domain for schema translations. Should match the domain in the `pybabel compile` command.
    schema_domain = 'schema'
    # The gettext domain for codelist translations. Should match the domain in the `pybabel compile` command.
    codelist_domain = 'codelist'

    schema_source_dir = basedir / 'schema'
    codelist_source_dir = basedir / 'schema' / 'codelists'
    schema_target_dir = static_dir
    codelist_target_dir = static_dir / 'codelists'

    translate([
        # The glob patterns in `babel_bods_schema.cfg` should match these filenames.
        (glob(str(schema_source_dir / '*.json')), schema_target_dir, schema_domain),
        # The glob patterns in `babel_bods_codelist.cfg` should match these.
        (glob(str(codelist_source_dir / '*.csv')), codelist_target_dir, codelist_domain),
    ], localedir, language, version=os.environ.get('TRAVIS_BRANCH', 'latest'))


def setup(app):
    language = app.config.overrides.get('language', 'en')
    translate_schema_and_codelists(language)
    app.add_directive('json-value', JSONValue)
    app.add_config_value('recommonmark_config', {
        #'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
        'enable_eval_rst': True
        }, True)
    app.add_transform(AutoStructify)
