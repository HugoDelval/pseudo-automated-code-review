from code_review import CodeReview


class Perl(CodeReview):
    def __init__(self, directory_path):
        super().__init__(directory_path)
        self.language = "PERL"
        self.exclude += ['"javascript"', '"\.pm:\#"', '"\.pl:\#"', "'Logger::'"]

    def launch_code_review(self):
        print("Launching PERL review for : " + self.directory_path)
        """
        For now we focus on system commands execution
        in PERL you can do it with :
        - open() : dangereux si contient un '|' ainsi qu'un '$' ou un '@' -> signifie que l'on ouvre un shell avec des paramètres (donc potentiellement des entrées utilisateurs)
        - `...`  : dangeureux si contient un '$' ou un '@' -> signifie que l'on ouvre un shell avec des paramètres (donc potentiellement des entrées utilisateurs)
        - exec() : dangeureux si contient un '$' ou un '@' -> signifie que l'on ouvre un shell avec des paramètres (donc potentiellement des entrées utilisateurs)
        - qx/({  : dangeureux si contient un '$' ou un '@' -> signifie que l'on ouvre un shell avec des paramètres (donc potentiellement des entrées utilisateurs)
        - use re 'eval' : permet d'executer des commandes via des regex
        """
        output_open = self.launch_command(
            'egrep "open[ |\(]+.+,.*[\$|\||@]" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'"
        )
        output_backticks = self.launch_command(
            "egrep '.*`.*\$.*`.*' " + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude + ['"SELECT"', '"FROM"', '"WHERE"', '"AND"', '"INSERT"',
                                                           '"INNER JOIN"', '"GRANT ALL"', '"DATABASE"',
                                                           '"hostname"']
                                           ) + " | grep -x '^.\{3,300\}'"
        )
        output_exec = self.launch_command(
            'egrep "exec[ |\(]+.*[\$|@]" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'"
        )
        output_qx = self.launch_command(
            'egrep "qx.+[\$|@]" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'"
        )
        output_system = self.launch_command(
            'egrep "system[ |\(]+.*[\$|@]" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'"
        )
        output_regex = self.launch_command(
            'grep "use re \'eval\'" ' + self.directory_path + ' -R 2> /dev/null |' +
            'grep -v ' + '| grep -v '.join(self.exclude) + " | grep -x '^.\{3,300\}'"
        )

        self.audit_results.update({
            "outputs": {
                "output_open": output_open,
                "output_backticks": output_backticks,
                "output_exec": output_exec,
                "output_qx": output_qx,
                "output_system": output_system,
                "output_regex": output_regex,
            },
            "nb_outputs": len(output_open) + len(output_backticks) + len(output_exec) + \
                          len(output_qx) + len(output_system) + len(output_regex)
        })
        return self.audit_results
