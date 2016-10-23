from code_review import CodeReview


class Ccpp(CodeReview):

    def __init__(self, directory_path):
        super().__init__(directory_path)
        self.language = "C_CPP"

    def launch_code_review(self):
        print("Launching C/C++ review for : " + self.directory_path)
        """
        """
        return self.audit_results
