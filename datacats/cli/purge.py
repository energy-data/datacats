# Copyright 2014-2015 Boxkite Inc.

# This file is part of the DataCats package and is released under
# the terms of the GNU Affero General Public License version 3.0.
# See LICENSE.txt or http://www.fsf.org/licensing/licenses/agpl-3.0.html

from os.path import isdir
from shutil import rmtree

from datacats.project import Project, ProjectError

def purge(opts):
    try:
        project = Project.load(opts['--project'])
    except ProjectError as e:
        try:
            project = Project.load(opts['--project'], data_only=True)
        except ProjectError:
            print e  # first error, not the second one
            return

    project.stop_web()
    project.stop_data_and_search()

    if opts['--delete-project']:
        if not project.target:
            print 'Failed to load project. Not deleting project directory.'
        else:
            project.fix_project_permissions()
            rmtree(project.target)

    project.purge_data()