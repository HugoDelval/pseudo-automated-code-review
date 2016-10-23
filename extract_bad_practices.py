#!/usr/bin/python3

import getpass
import operator
import os
import requests
import subprocess

import sys

import time
from bs4 import BeautifulSoup
import config

letter_end = '-'


def create_bash():
    return subprocess.Popen(['/bin/bash'], universal_newlines=True, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)


def detect_language(current_repo_path):
    grep_v = ''
    if config.EXCLUDE:
        grep_v = 'grep -v ' + '| grep -v '.join(config.EXCLUDE)
    total = int(
        create_bash().communicate(input='find ' + current_repo_path + " -type f | " + grep_v + " | wc -l")[0][:-1])
    scores = {}
    scores['perl'] = (int(create_bash().communicate(
        input='find ' + current_repo_path + " -regextype sed -regex '.*/.*\.p[m|l]' | " + grep_v + " | wc -l ")[0][
                          :-1]), config.PERL)
    scores['python'] = (int(
        create_bash().communicate(input='find ' + current_repo_path + " -name '*.py' | " + grep_v + " | wc -l ")[0][
        :-1]), config.PYTHON)
    scores['go'] = (int(
        create_bash().communicate(input='find ' + current_repo_path + " -name '*.go' | " + grep_v + " | wc -l ")[0][
        :-1]), config.GO)
    scores['c_cpp'] = (int(create_bash().communicate(
        input='find ' + current_repo_path + " -regextype sed -regex '.*/.*\.[c|h]p\{0,2\}' | " + grep_v + " | wc -l ")[
                               0][:-1]), config.C_CPP)
    scores['js'] = (int(
        create_bash().communicate(input='find ' + current_repo_path + " -name '*.js' | " + grep_v + " | wc -l ")[0][
        :-1]), config.JS)
    scores['java'] = (int(
        create_bash().communicate(input='find ' + current_repo_path + " -name '*.java' | " + grep_v + " | wc -l ")[0][
        :-1]), config.JAVA)
    maximum_score = max(scores.items(), key=operator.itemgetter(1))[1]
    if maximum_score[0] is 0:
        maximum_score = (0, config.UNKNOWN)
        output_robot = set(
            create_bash().communicate(input='find ' + current_repo_path + ' -iname "*robot*" 2> /dev/null'
                                      ) + create_bash().communicate(
                input='find ' + current_repo_path + ' -iname "*todo*" 2> /dev/null'
            ))
        try:
            output_robot.remove('')
        except:
            pass
        if len(output_robot) > 1:
            print("-------------------------------------------------------------------------------")
            print(config.languages[config.UNKNOWN] + " but found " + str(
                len(output_robot)) + " robots directories/files here : " + current_repo_path)
            print("Here there are : " + str(output_robot))
            print('You may need to add this language..?')
            print("-------------------------------------------------------------------------------")

    return maximum_score[1]


def create_directories_and_detect_languages():
    subprocess.call(["mkdir", '-p', config.REPO_BASE])
    directories_with_languages = []
    for project in open('projects'):
        project = project[:-1]
        repo_name, ssh_clone_url = project.split(' ')
        print(repo_name, ssh_clone_url)
        time.sleep(0.5)
        current_repo_path = os.path.join(config.REPO_BASE, repo_name)
        print("---- Checkout " + ssh_clone_url + " into " + repo_name + " ----")
        try:
            age_of_git_dir = time.time() - os.path.getmtime(current_repo_path)
            if age_of_git_dir > 60 * 60 * 24 * config.NB_JOURS_BEFORE_DELETING_REPO:
                subprocess.call(['rm', '-rf', current_repo_path])
                subprocess.call(
                    ['git', 'clone', "--quiet", "--single-branch", "--depth=1", ssh_clone_url,
                     current_repo_path])
        except FileNotFoundError as e:
            subprocess.call(
                ['git', 'clone', "--quiet", "--single-branch", "--depth=1", ssh_clone_url,
                 current_repo_path])
        except Exception as e:
            print("\n++++ Weird exception here : " + str(e) + "\n")
        if not os.path.isdir(current_repo_path):
            continue
        project_language = detect_language(current_repo_path)
        directories_with_languages.append(
            {'path': current_repo_path, 'language': config.languages[project_language]})
        print("Language detected : " + config.languages[project_language])
            

    with open(config.OUTPUTS, "w") as f:
        import json
        f.write(json.dumps(directories_with_languages))


if __name__ == "__main__":
    from_json_directly = len(sys.argv) == 2
    if not from_json_directly:
        create_directories_and_detect_languages()
    from audit import Audit

    my_audit = Audit(config.OUTPUTS)
    my_audit.launch_audit()
