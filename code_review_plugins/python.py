from code_review import CodeReview


class Python(CodeReview):
    def __init__(self, directory_path):
        super().__init__(directory_path)
        self.language = "PYTHON"
        self.exclude += ['"javascript"', '"\.py:\#"']

    def launch_code_review(self):
        print("Launching Python review for : " + self.directory_path)
        """
        In python, in general the system commands are called securely. But we have to check for
        - commands         # really old (python2)
        - shell=True       # from subprocess
        - os.command
        - os.popen
        - os.system
        - cPickle.loads    # why not ?
        """
        output_commands = self.launch_command(
            'egrep "getstatusoutput|getoutput" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")
        output_shell = self.launch_command(
            'grep "shell=True" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")
        output_oscommand = self.launch_command(
            'egrep "command[ ]*(" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")
        output_ospopen = self.launch_command(
            'egrep "popen[ ]*(" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")
        output_ossystem = self.launch_command(
            'egrep "system[ ]*(" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")
        output_pickle = self.launch_command(
            'grep "cPickle.loads" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")

        self.audit_results.update({
            "output": {
                "output_commands": output_commands,
                "output_shell": output_shell,
                "output_command": output_oscommand,
                "output_ospopen": output_ospopen,
                "output_ossystem": output_ossystem,
                "output_pickle": output_pickle
            },
            "nb_outputs": len(output_shell) + len(output_oscommand) + len(output_pickle) + len(output_commands) + len(
                output_ospopen) + len(output_ossystem)
        })
        return self.audit_results
