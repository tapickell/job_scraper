"""
Module Doc String
"""
import json
import pprint
import re
from linkedin_api import Linkedin

with open("credentials.json", "r") as f:
    credentials = json.load(f)

    if credentials:
        linkedin = Linkedin(credentials["username"], credentials["password"])

        found_langs = {}
        for offset in range(21):
            for job in linkedin.search_jobs(
                keywords="software engineer",
                experience=["4"],
                job_type=["F", "C"],
                location_name="United States",
                remote=["2"],
                limit=49,
                offset=offset
            ):
                job_id = job["entityUrn"].split(":")[3]
                job_data = linkedin.get_job(job_id=job_id)
                description_text = job_data["description"]["text"].lower()
                print("Job Found:")
                pprint.pp(job_data["title"])
                pprint.pp(job_data["jobPostingId"])

                langs = ["ruby", "elixir", "node.js", "typescript", "golang", "go", "python",
                         "java", "clojure", "scala", "haskell", "lisp", "rust", "swift",
                         "kotlin", "c++", "c#", "react", "vuejs", "javascript", "elm",
                         "groovy", "f#", "ocaml", "smalltalk", "scheme", "racket", "php",
                         "objective-c", "flutter", "dart", "lua", "perl", "erlang", "gleam",
                         "clojerl", "hcl", "crystal", "julia", "zig", "fortran", "cobol",
                         "prolog", "ada", "nim", "postgresql", "mysql", "mongodb", "redis",
                         "mariadb", "elasticsearch", "snowflake", "neo4j", "flask", "django",
                         "angular", "phoenix", "rails", ".net", "pytorch", "spring", "gql"]

                for lang in langs:
                    reg = r"\s%s[\s,]" % re.escape(lang)
                    maybe_found = re.findall(reg, description_text)
                    if maybe_found != []:
                        [l, *_] = maybe_found
                        l_key = l.strip(",").strip()
                        found_langs.setdefault(l_key, 0)
                        found_langs[l_key] += 1
                        print("%s: %s" % (l_key, found_langs[l_key]))

        pprint.pp(found_langs)
