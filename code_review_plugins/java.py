from code_review import CodeReview


class Java(CodeReview):
    def __init__(self, directory_path):
        super().__init__(directory_path)
        self.language = "JAVA"
        self.exclude += ['"javascript"', '"\.java://"', '"System.out.println"', '"\.csv"', '" LOG\."', '"\.xml"']

    def launch_code_review(self):
        print("Launching Java review for : " + self.directory_path)
        """
        Seems that Java handle quite well the execution of system commands. We can try looking for :
        - .exec(
        - 'sh' + '-c'
        """
        output_exec = self.launch_command(
            'grep "\.exec(" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")
        output_bash = self.launch_command(
            'egrep "sh.*-c" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")

        self.audit_results.update({
            "output": {
                "output_exec": output_exec,
                "output_bash": output_bash,
            },
            "nb_outputs": len(output_exec) + len(output_bash)
        })
        return self.audit_results
