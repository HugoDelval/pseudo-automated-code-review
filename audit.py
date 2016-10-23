import sys
import json

from code_review import CodeReview
from code_review_plugins.ccpp import Ccpp
from code_review_plugins.go import Go
from code_review_plugins.java import Java
from code_review_plugins.js import Js
from code_review_plugins.perl import Perl
from code_review_plugins.python import Python


def get_tuple_sort(x):
    try:
        return -(x['code_review']['is_robot']), -(x['code_review']['nb_outputs'])
    except:
        return 99999999, 99999999


class Audit:
    def __init__(self, json_file):
        self.json_file = json_file
        with open(json_file) as f:
            content = f.read()
            self.repositories = json.loads(content)
        if not self.repositories:
            print("Error reading " + json_file + " file.")
            sys.exit(1)

    def launch_audit(self):
        print("\n---------- Starting Audit ----------\n")
        for index, repository in enumerate(self.repositories):
            if repository['language'] == 'UNKNOWN':
                # print(
                #     'You can add a plugin in /code_review_plugins/ if you want to contribute.')
                code_review = CodeReview(repository['path'])
            elif repository['language'] == 'PERL':
                code_review = Perl(repository['path'])
            elif repository['language'] == 'JAVA':
                code_review = Java(repository['path'])
            elif repository['language'] == 'GO':
                code_review = Go(repository['path'])
            elif repository['language'] == 'PYTHON':
                code_review = Python(repository['path'])
            elif repository['language'] == 'C_CPP':
                code_review = Ccpp(repository['path'])
            elif repository['language'] == 'JS':
                code_review = Js(repository['path'])
            else:
                # print(
                #     'Sorry, unknown language. You can add a plugin in /code_review_plugins/ if you want to contribute.')
                continue
            self.repositories[index]['code_review'] = code_review.launch_code_review()
        self.repositories = sorted(self.repositories, key=lambda x: get_tuple_sort(x))
        with open(self.json_file, "w") as f:
            f.write(json.dumps(self.repositories, indent=4, sort_keys=True))
            print("Outputs were written in " + self.json_file)
