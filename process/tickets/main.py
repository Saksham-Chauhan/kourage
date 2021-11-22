from helper.redmine import RedmineConfig


# TODO => Show opened issues
# TODO => Show resolved issues
# TODO => Add issue name along with id in spent time


def get_open_issues():
    redmine = RedmineConfig().initialize()

    issues = redmine.issue.filter(status='open')
    return issues
