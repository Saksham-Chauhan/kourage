from helper.redmine import RedmineConfig

redmine = RedmineConfig().initialize()

project = redmine.project.get('kore')
