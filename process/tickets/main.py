from helper.redmine import RedmineConfig
from redminelib.exceptions import ResourceAttrError


# TODO => Add issue name along with id in spent time


def get_open_issues():
    redmine = RedmineConfig().initialize()
    issues = redmine.issue.filter(status='open')
    return issues


def get_resolved_issues():
    redmine = RedmineConfig().initialize()
    issues = redmine.issue.filter(status='resolved')
    return issues


def prepare_embed_message(issues):
    message = str()
    for issue in issues:
        try:
            message += issue['id'] + " - " + issues['subject'] + " - " + issues['assigned_to']
        except ResourceAttrError:
            message += issue['id'] + " - " + issues['subject'] + " - " + "_Please assign this_"
    return message
