from code_review import CodeReview


class Go(CodeReview):
    def __init__(self, directory_path):
        super().__init__(directory_path)
        self.language = "GO"
        self.exclude += ['"javascript"']

    def launch_code_review(self):
        print("Launching Go review for : " + self.directory_path)
        """
        Don't really know what's wrong with golang :p Let's try this blindly :
        - "Command" + "-c" (may possibly result in sh -c "inject here please")
        """
        output_command = self.launch_command(
            'egrep "Command.*-c" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'")

        self.audit_results.update({
            "output": {
                "output_command": output_command,
            },
            "nb_outputs": len(output_command)
        })
        return self.audit_results
