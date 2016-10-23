PERL = 1
PYTHON = 2
GO = 3
C_CPP = 4
JS = 5
UNKNOWN = 6
JAVA = 7

languages = {
    PERL: 'PERL',
    PYTHON: 'PYTHON',
    GO: 'GO',
    C_CPP: 'C_CPP',
    JS: 'JS',
    UNKNOWN: 'UNKNOWN',
    JAVA: 'JAVA',
}

OUTPUTS = 'outputs.json'
REPO_BASE = "git-repositories"
EXCLUDE = ['.git']
NB_JOURS_BEFORE_DELETING_REPO = 7
