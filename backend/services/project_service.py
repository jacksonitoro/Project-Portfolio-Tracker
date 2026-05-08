from models import Project

def calculate_variance(project):
    return project.budget - project.actual_cost


def determine_status(project):

    if project.actual_cost > project.budget:
        return "Over Budget"

    elif (
        project.progress < 50 and
        project.actual_cost > project.budget * 0.7
    ):
        return "At Risk"

    elif project.progress >= 80:
        return "On Track"

    else:
        return "Delayed"


def process_project(project):
    project.status = determine_status(project)
    return project