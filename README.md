Beneficial Ownership Data Standard
==================================

This repository contains work in progress for the development of a data specification and standard for publication and consumption of data about Beneficial Ownership.

You can find the latest draft of the schema and documentation for review at [http://standard.openownership.org/](http://standard.openownership.org/)

You can share feedback on the standard through this project's issue tracker.

## About

This work is taking place under the auspices of the Open Ownership project. More details on the project are available at http://www.openownership.org

The work will be guided by the Data Standard Working Group, and initial phases will take place between December 2016 and March 2017.

### Contact

For more details about the Open Ownership project, please contact the project coordinator, [Zosia Sztykowski](mailto:zosia@openownership.org)

### Partners and funders

The initial development of the Beneficial Ownership Data Standard is funded through support for the Open Ownership project from the UK Department for International Development. Open Ownership is a project of [Transparency International](https://www.transparency.org/), [One](https://www.one.org/international/), the [Open Contracting Partnership](http://www.open-contracting.org), the [World Wide Web Foundation](http://www.webfoundation.org), [Global Witness](https://www.globalwitness.org/en-gb/) and [The B Team](http://bteam.org/)

## Technical documentation

### Build the docs locally

Please see https://github.com/openownership/data-standard-sphinx-theme

### Translation

Translation consists of generating strings to be translated from the English docs, pushing them to Transifex, fetching translations back from Transifex, and then you can build the docs in the other languages you need.

To run the steps in the translation workflow, you need to install this repo and its dependencies in your local environment.

```
$ pip install -r requirements.txt
```

You also need to make sure you have `gettext` and `pybabel` installed in whatever environment you're running this in:

```
$ apt-get install gettext
$ apt-get install python-babel
```

And you need to get a [Transifex API key](https://www.transifex.com/user/settings/api/), make sure you have access to the [BODS project on Transifex](https://www.transifex.com/OpenDataServices/bods-v01)

**When you add or update the docs** you need to do the following so that they can be translated, in the `docs` directory:

1. Run `make gettext` to extract translatable English strings from the docs.
2. Run `pybabel extract -F babel_bods_codelist.cfg . -o docs/locale/codelist.pot` to extract translatable English strings from the codelists.
2. Run `pybabel extract -F babel_bods_schema.cfg . -o docs/locale/schema.pot` to extract translatable English strings from the schema.
2. *If you have new pages* run `sphinx-intl update-txconfig-resources --pot-dir _build/gettext --transifex-project-name bods-v01` to register the translation files with Transifex (generates or updates contents `.tx/config` file).
3. Run `tx push -s` to push to Transifex.

Now the files are ready to be translated in Transifex.

**To fetch new translations** when they're done, you need to:

1. Run `tx pull -a` to fetch all, or `tx pull -l ru` to fetch a particular language.
2. Compile the schema and codelist translations:

```
$ pybabel compile --use-fuzzy -d docs/locale -D schema
$ pybabel compile --use-fuzzy -d docs/locale -D codelist
```

**To build another language locally** (pass the language code you want)..

```
$ cd docs
$ sphinx-build -b html -D language=ru . _build/html/ru
```



<!-- # Directory in which to build documentation files.
BUILD_DIR=build

# Directory in which to build .pot files.
POT_DIR=$(BUILD_DIR)/locale

# Directory of catalog files.
LOCALE_DIR=docs/locale -->

<!--
    pybabel compile --use-fuzzy -d $(LOCALE_DIR) -D $(DOMAIN_PREFIX)schema
pybabel compile --use-fuzzy -d $(LOCALE_DIR) -D $(DOMAIN_PREFIX)codelists
-->