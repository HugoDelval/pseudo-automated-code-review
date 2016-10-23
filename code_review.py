#!/usr/bin/python3
import subprocess


# from abc import ABC, abstractmethod


class CodeReview:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.exclude = ['"Binary file "', '"\.svn"', '"\.git"', '"Fichier binaire "', "'static/'",
                        "'jquery'", "'OpenLayers.js'", "'highlight.js'", "'bower_components/'",
                        "'swagger-ui/'", "'frontend'"]
        output_robot = len(set(self.launch_command(
            'find ' + self.directory_path + ' -iname "*robot*" 2> /dev/null'
        ) + self.launch_command(
            'find ' + self.directory_path + ' -iname "*todo*" 2> /dev/null'
        )))
        self.audit_results = {'is_robot': output_robot, 'nb_outputs': 0}

    def launch_code_review(self):
        return self.audit_results

    @staticmethod
    def launch_command(cmd):
        try:
            responses = subprocess.check_output(['/bin/bash', "-c", cmd]).splitlines()
        except subprocess.CalledProcessError as e:
            responses = []
        if '' in responses:
            responses.remove('')
        try:
            for index, response in enumerate(responses):
                responses[index] = response.decode('utf-8', 'ignore')
        except Exception as e:
            print(e)
            return []
        return responses


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage : " + __file__ + " review_db.json")
        print("""Here is what a review_db.json should look like :
[
    {
        "language": "PYTHON",
        "path": "/path/to/python/git/repo"
    },
    {
        "language": "GO",
        "path": "relative/path/to/go/git/repo"
    },
    {
        "language": "JAVA",
        "path": "relative/to/JAVA/git/repo"
    }
]""")
        sys.exit(1)
    json_file = sys.argv[1]
    from audit import Audit

    my_audit = Audit(json_file)
    my_audit.launch_audit()
