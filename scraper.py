"""
Module Doc String
"""
import csv
import datetime
import json
from pathlib import Path
import pprint
import re
from linkedin_api import Linkedin

def company_name(company_data):
    "Get the company name from the nested company_data strucutre"
    return company_data['com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany']['companyResolutionResult']['name']

def apply_url(apply_data):
    "unwraps the apply data structure to get at the apply url"
    unwrapped = list(apply_data.values())[0]
    return list(unwrapped.values())[1]

with open("credentials.json", "r", encoding="utf-8") as f:
    credentials = json.load(f)
    file_path = f"results_{str(datetime.datetime.now()).replace(" ", "_")}.csv"
    Path(file_path).touch()

    if credentials:
        linkedin = Linkedin(credentials["username"], credentials["password"])
        with open(file_path, 'w', encoding="utf-8", newline='') as csv_file:
            field_names = ['title', 'technology', 'posting_id', 'apply_method', 'company']
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(field_names)

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
                    title = job_data["title"]
                    posting_id = job_data["jobPostingId"]
                    company = company_name(job_data["companyDetails"])
                    apply_method = apply_url(job_data["applyMethod"])
                    pprint.pp(title)
                    pprint.pp(posting_id)

                    langs = ["ruby", "elixir", "nodejs", "node", "node.js",
                             "typescript", "golang", "go", "python", "functional",
                             "java", "clojure", "scala", "haskell", "lisp", "rust", "swift",
                             "kotlin", "c++", "c#", "react", "vuejs", "javascript", "elm",
                             "groovy", "f#", "ocaml", "smalltalk", "scheme", "racket", "php",
                             "objective-c", "flutter", "dart", "lua", "perl", "erlang", "gleam",
                             "clojerl", "hcl", "crystal", "julia", "zig", "fortran", "cobol",
                             "prolog", "ada", "nim", "postgresql", "mysql", "mongodb", "redis",
                             "mariadb", "elasticsearch", "snowflake", "neo4j", "flask", "django",
                             "angular", "phoenix", "rails", ".net", "pytorch", "spring", "gql",
                             "ios", "android", "concurency", "senior"]

                    technology = []
                    for lang in langs:
                        reg = fr"\s{re.escape(lang)}[\s,]"
                        maybe_found = re.findall(reg, description_text)
                        if maybe_found != []:
                            [l, *_] = maybe_found
                            l_key = l.strip(",").strip()
                            found_langs.setdefault(l_key, 0)
                            found_langs[l_key] += 1
                            technology.append(l_key)
                            print(f"{l_key}: {found_langs[l_key]}")

                    csv_writer.writerow([title,
                         str(technology),
                         posting_id,
                         str(apply_method),
                         str(company)])

            # sort by number Found
            # include a total of number searched
            pprint.pp(found_langs)
