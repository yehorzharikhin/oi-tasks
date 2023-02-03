import json
import os


def test_filenames():
    def make_error(text):
        print(text)
        assert False
    folder_dir = os.path.join(os.path.dirname(__file__), '..')
    with open(os.path.join(folder_dir, 'languages.json'), 'r') as f:
        languages = json.load(f)
    statements_dir = os.path.join(folder_dir, 'statements')
    for contest in os.listdir(statements_dir):
        contest_path = os.path.join(statements_dir, contest)
        if os.path.isdir(contest_path):
            for year in os.listdir(contest_path):
                if year == '.DS_Store':
                    continue
                if not year.isdigit():
                    make_error('year folder is not int ' + year)
                if int(year) < 1980 or int(year) > 2030:
                    make_error('wrong year ' + year)
                year_path = os.path.join(contest_path, year)
                problems = 0
                max_problem = 0
                for problem in os.listdir(year_path):
                    if problem == '.DS_Store':
                        continue
                    if not problem.isdigit():
                        make_error('problem folder is not int ' + problem)
                    if int(problem) <= 0 or int(problem) > 8:
                        make_error('wrong problem ' + problem)
                    problems += 1
                    max_problem = max(max_problem, int(problem))
                    problem_path = os.path.join(year_path, problem)
                    has_isc = False
                    for statement in os.listdir(problem_path):
                        parts = statement.split('-')
                        if len(parts) != 4:
                            make_error('wrong filename ' + statement)
                        if parts[0] != contest:
                            make_error('wrong contest in filename ' + statement)
                        if parts[1] != year:
                            make_error('wrong year in filename ' + statement)
                        if parts[2] != problem:
                            make_error('wrong problem in filename ' + statement)
                        name = parts[3]
                        if len(name) != 10:
                            make_error('wrong length of filename ' + statement)
                        if name[2] != '_' or name[6:] != '.pdf':
                            make_error('wrong format of filename ' + statement)
                        if name == 'en_ISC.pdf':
                            has_isc = True
                        language = name[:2]
                        country = name[3:6]
                        if language not in languages:
                            make_error('languages not found ' + statement)
                        if country not in languages[language]:
                            make_error('country not found ' + statement)
                    if not has_isc:
                        make_error('Does not have ISC version ' + problem_path)

                if max_problem != problems:
                    make_error('not consecutive problems')


