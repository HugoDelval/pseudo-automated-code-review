from code_review import CodeReview


class Js(CodeReview):
    def __init__(self, directory_path):
        super().__init__(directory_path)
        self.exclude += []
        self.language = "JS"

    def launch_code_review(self):
        print("Launching JS review for : " + self.directory_path)
        """
        Assuming nodeJS :
        - new run_cmd( ...
        - exec( ...
        - spawn( ...
        """
        output_run_cmd = self.launch_command(
            'egrep "run_cmd[ |\(]+" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'"
        )
        output_exec = self.launch_command(
            'egrep "exec[ |\(]+" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'"
        )
        output_spawn = self.launch_command(
            'egrep "spawn[ |\(]+" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'"
        )

        self.audit_results.update({
            "outputs": {
                "output_run_cmd": output_run_cmd,
                "output_exec": output_exec,
                "output_spawn": output_spawn,
            },
            "nb_outputs": len(output_spawn) + len(output_run_cmd) + len(output_exec)
        })

        return self.audit_results