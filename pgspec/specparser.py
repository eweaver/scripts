import subprocess
from subprocess import Popen, PIPE

class SpecParser:
    APP_DIRECTORY = "/app"
    SPEC_DIRECTORY = "/spec"

    def specs_from_changes(self, changes, directory):
        specs = []

        if directory:
            path = directory[1:] + "/"
        else:
            path = ""

        for regex_results in changes:
            if isinstance(regex_results, basestring):
                file_path = regex_results
            else:
                if regex_results[0] == "spec":
                    spec_name = regex_results[1]
                else:
                    spec_name = regex_results[1].replace('.rb', '_spec.rb')

                file_path = "spec" + spec_name

            specs.append(path + file_path)

        return specs

    def iterate_spec_files(files):
        return_files = []
        for file, definition in files.iteritems():
            idx = find_specific_test_cases(file, definition)
            return_files.append(file, idx)

        return return_files

    def find_specific_test_cases(self, file, definition):
        definition_line = -1

        with open ("../spec/" + file.replace('.rb', '_spec.rb'), "r") as data:
            idx = 1
            for line in data:
                r = re.compile('describe\s*[\'\"]{1}' + definition[0] + '[\'\"]{1}', re.IGNORECASE)
                spec_match = r.findall(line)
                if spec_match:
                    definition_line = idx
                    break

                idx += 1

        return definition_line
