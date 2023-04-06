from os import getenv

from setuptools import setup

from merge_queue_experiment import __version__ as base_version


def determine_pull_request_build_version(build_suffix: str) -> str:
    change_target = getenv("CHANGE_TARGET", "")
    branch = getenv("CHANGE_BRANCH", "")

    if branch.startswith("feature") and change_target != "master":
        # PR from feature to development -> beta
        return base_version + "b" + build_suffix
    elif branch.startswith("release") or branch.startswith("hotfix"):
        # PR from release or hotfix branch -> release candidate
        return base_version + "rc" + build_suffix
    else:
        raise ValueError(f"Cannot build for pull request from '{branch}' into '{change_target}'")


def determine_branch_build_version(build_suffix: str) -> str:
    branch = getenv("BRANCH_NAME", "")

    if branch.startswith("master"):
        return base_version
    elif branch.startswith("main"):
        return base_version + "b0" + build_suffix
    else:
        raise ValueError(f"Cannot build for branch '{branch}'")


def determine_build_version() -> str:
    if not getenv("JENKINS_HOME", False):
        return base_version

    build_suffix = getenv("CHANGE_ID", "") + ".dev" + getenv("BUILD_NUMBER")

    if getenv("BRANCH_NAME", "").startswith("PR-"):
        return determine_pull_request_build_version(build_suffix)

    return determine_branch_build_version(build_suffix)


build_version = determine_build_version()
print("********************")
print(f"Building version: {build_version}")
print("********************")


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="public-merge-queue-experiment",
    packages=[
        "merge_queue_experiment",
    ],
    url="https://github.com/calendar42/public-merge-queue-experiment",
    author="Plotwise",
    author_email="",
    description="Merge queue experiment",
    long_description=long_description,
    version=build_version,
)
