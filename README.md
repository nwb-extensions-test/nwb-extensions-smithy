Overview
--------

`nwb-extensions-smithy` is a tool for combining an NWB extension with configurations to build using freely hosted CI services into a single repository, also known as a feedstock.
`nwb-extensions-smithy` is still a work-in-progress, but when complete, `nwb-extensions-smithy` will:

+ Create a git repo with an NWB extension and the files to test the extension using CI services.
+ Register the repo on GitHub and push it.
+ Connect the repo to Circle CI and Azure Pipelines

This code was adapted from [conda-smithy](https://github.com/conda-forge/conda-smithy).

Installation
------------

The easiest way to install conda-smithy is to use conda and conda-forge:

```
conda install -n root -c conda-forge conda-smithy
```

To install conda-smithy from source, see the requirements file in `requirements.txt`, clone this
repo, and `python -m pip install .`.

Setup
-----

You need a token from github, travis-ci.org, appveyor.com and circleci.com to try out
`conda-smithy`. The commands which need this will tell you where to get these tokens and where to
place them. If you need help getting tokens please ask on the
[conda-forge google group](https://groups.google.com/forum/?hl=en#!forum/conda-forge).

You should be able to test parts of `conda-smithy` with whatever tokens you have.
For example, you should be able to `conda smithy register-github` without the CI service tokens.
Re-rendering an existing feedstock is also possible without CI service tokens set.

Re-rendering an existing feedstock
----------------------------------

Periodically feedstocks need to be upgraded to include new features. To do
this we use `conda-smithy` to go through a process called re-rendering.
Make sure you have installed `conda-smithy` before proceeding.
Re-rendering an existing feedstock is possible without CI service tokens set.

1. `cd <feedstock directory>`
2. `conda smithy rerender [--commit]`
3. Commit and push all changes

Optionally one can commit the changes automatically with `conda-smithy` version `1.4.1+`.
To do this just use the `--commit`/`-c` option. By default this will open an editor to make a commit.
It will provide a default commit message and show the changes to be added. If you wish to do this
automatically, please just use `--commit auto`/`-c auto` and it will use the stock commit message.

Making a new feedstock
----------------------

1. **Make the feedstock repo:** `conda smithy init
<directory_of_conda_recipe>`.     For a recipe called `foo`, this creates a
directory called `foo-feedstock`, populates it with CI setup skeletons, adds the recipe under
`recipe` and initializes it as a git repo.
2. **Create a github repo:** `conda smithy register-github --organization conda-forge ./foo-feedstock`.
This requires a github token. You can try it out with a github user account
instead of an organization by replacing the organization argument with
`--user github_user_name`. If you are interested in adding teams for your feedstocks,
you can provide the `--add-teams` option to create them. This can be done when creating
the feedstock or after.
3. **Register the feedstock with CI services:**
`conda smithy register-ci --organization conda-forge --feedstock_directory ./foo-feedstock`.
This requires tokens for the CI services. You can give the name of a user instead
of organization with `--user github_user_name`.
4. **Specify the feedstock channel and label:**
Optionally, you can specify source channels and choose a channel to upload to in `recipe/conda_build_config.yaml`.
  ```yaml
  channel_sources:
    - mysourcechannel1,mysourcechannel2,conda-forge,defaults
  channel_targets:
    - target_channel target_label
  ```
  Default source channels are `conda-forge,defaults`. Default for channel targets is `conda-forge main`.

5. **Re-render the feedstock:** ``conda smithy rerender --feedstock_directory ./foo-feedstock``
6. **Commit the changes:** ``cd foo-feedstock && git commit``, then push ``git push upstream master``.

Running a build
---------------

When everything is configured you can trigger a build with a push to the feedstock repo on github.

Releasing conda-smithy
----------------------
To release a new version of conda-smithy, you can use the
[rever](https://regro.github.io/rever-docs/index.html) release managment tool.
Run `rever` in the root repo directory with the version number you want to release.
For example,

```sh
$ rever 0.1.2
```


Conda-smithy in a nutshell
--------------------------

#### xkcd 1629: Tools

[![xkcd 1629: Tools](https://imgs.xkcd.com/comics/tools.png)](https://xkcd.com/1629/)

**Titletext**: *I make tools for managing job-hunting sites for people who make*
*tools for managing job-hunting sites for people who make tools for ...*
