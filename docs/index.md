# Table of contents

Baserow is an open-source online database tool. Users can use this no-code platform to
create a database without any technical experience. It lowers the barriers to app
creation so that anyone who can work with a spreadsheet can also create a database. The
interface looks a lot like a spreadsheet. Our goal is to provide a perfect and fast user
experience while keeping it easy for developers to write plugins and maintain the
codebase. The developer documentation contains several topics you might need as a
developer.

## Installation

We provide a hosted version of Baserow which you can sign up and start using immediately
at [https://baserow.io](https://baserow.io). Alternatively you can easily self-host
Baserow by following one the guides below:

* [Install with Docker](installation/install-with-docker.md): A step-by-step guide to
  install Baserow using docker.
* [Install with Docker Compose](installation/install-with-docker.md): A step-by-step
  guide to install Baserow using Docker Compose.
* [Install on Cloudron](installation/install-on-cloudron.md): Instructions to manually
  install Baserow on Cloudron.
* [Install on Heroku](installation/install-on-heroku.md): A step-by-step guide to
  install Baserow using Heroku.
* [Migrate from Ubuntu to Docker](installation/migrate-from-ubuntu-to-docker.md): If you
  have previously installed Baserow using the deprecated ubuntu guide below then please
  follow this guide to migrate your install to use the new Docker install.
* [DEPRECATED: Install on Ubuntu](installation/install-on-ubuntu.md): A deprecated and
  now unsupported guide on how to manually install Baserow and its required services on
  a fresh ubuntu install. Please use the guides above instead.

## Baserow Tutorials

* [Baserow Quick-start Tutorial](tutorials/quick-start.md): A quick introduction on how
  to use Baserow.
* [Understanding Baserow Formulas](tutorials/understanding-baserow-formulas.md): A
  tutorial explaining how to use the formula field in Baserow.

## API Usage

Baserow provides various APIs detailed below:

* [REST API](apis/rest-api.md): An introduction to the REST API and information about
  API resources.
* [WebSocket API](apis/web-socket-api.md): An introduction to the WebSockets API which
  is used to broadcast real time updates.

## Technical Overviews

* [Introduction](technical/introduction.md): An introduction to some important technical
  concepts in Baserow.
* [Database plugin](technical/database-plugin.md) An introduction to the database plugin
  which is installed by default.
* [Formula Technical Guide](technical/formula-technical-guide.md): A more technical
  guide about formulas aimed at developers who want to understand and work with
  internals of Baserow formulas.

## Development

Everything related to contributing and developing for Baserow.

* [Development environment](./development/development-environment.md): More detailed
  information on baserow's local development environment.
* [Running the Dev Environment](development/running-the-dev-environment.md): A
  step-by-step guide to run Baserow for development.
* [Directory structure](./development/directory-structure.md): The structure of all the
  directories in the Baserow repository explained.
* [Tools](./development/tools.md): The tools (flake8, pytest, eslint, etc) and how to
  use them.
* [Code quality](./development/code-quality.md): More information about the code style,
  quality, choices we made, and how we enforce them.
* [Create a template](./development/create-a-template.md): Create a template that can be
  previewed and installed by others.
* [dev.sh](./development/dev_sh.md): Further details on how to use Baserow's `./dev.sh`
  helper script.

- [IntelliJ setup](./development/intellij-setup.md): How to configure Intellij to work
  well with Baserow for development purposes.

## FAQs

* [Baserow Docker How To](delete/baserow-docker-how-to.md): Common operations and
  solutions for working with baserow's docker environments.

## Reference

* [Baserow Docker API](technical/baserow-docker-api.md): An API reference with all
  supported environment variables, command line arguments and usage patterns for
  Baserow's docker images and compose files.

## Plugins

Everything related to custom plugin development.

* [Plugin basics](./plugins/introduction.md): An introduction into Baserow plugins.
* [Plugin boilerplate](./plugins/boilerplate.md): Don't reinvent the wheel, use the
  boilerplate for quick plugin development.
* [Create application](./plugins/application-type.md): Want to create an application
  type? Learn how to do that here.
* [Create database table view](./plugins/view-type.md): Display table data like a
  calendar, Kanban board or however you like by creating a view type.
* [Create database table view filter](./plugins/view-filter-type.md): Filter the rows of
  a view with custom conditions.
* [Create database table field](./plugins/field-type.md): You can store data in a custom
  format by creating a field type.
* [Creata a field converter](./plugins/field-converter.md): Converters alter a field and
  convert the related data for specific field changes.

## Other

* [External resources related to Baserow](./other/external-resources.md): A list of
  external third party resources.
