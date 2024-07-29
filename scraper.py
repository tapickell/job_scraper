"""
Module Doc String
"""

import csv
import datetime
from decimal import Decimal
import json
from pathlib import Path
import pprint
import random
import re
from time import sleep
from linkedin_api import Linkedin

def date_string():
    "a formatted datestring"
    str(datetime.datetime.now()).replace(" ", "_")

def company_name(company_data):
    "Get the company name from the nested company_data strucutre"
    return company_data[
        "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"
    ]["companyResolutionResult"]["name"]

def apply_url(apply_data):
    "unwraps the apply data structure to get at the apply url"
    unwrapped = list(apply_data.values())[0]
    return list(unwrapped.values())[1]

def consolidate_technology(tech_term):
    "Consolidates tech terms to ensure totals are combined"
    match tech_term:
        case "go":
            return "golang"
        case "node" | "nodejs":
            return "node.js"
        case "gql":
            return "graphql"
        case _:
            return tech_term

def unwrap_salary(insights):
    "unwrap salary from secondary api call"
    match insights['insightExists']:
        case 'True' | True:
            return insights['compensationBreakdown']
        case _:
            return []

def default_evade():
    """
    A catch-all method to try and evade suspension from Linkedin.
    Currenly, just delays the request by a random (bounded) time
    """
    sleep(random.randint(2, 5))  # sleep a random duration to try and evade suspention

def fetch(li, uri: str):
    """GET request to Linkedin API"""
    default_evade()

    url = f"{li.client.API_BASE_URL}{uri}"
    return li.client.session.get(url)

def get_posting(li, post_id):
    "hack to get another api call from the client without updating the package"
    res = fetch(li,
                f"/jobs/jobPostings/{post_id}"
                f"?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65&"
                f"topN=1&"
                f"topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)"
                )
    data = res.json()
    return data

def get_card(li, card, posting_urn):
    "hack to get another api call from the client without updating the package"
    res = fetch(li,
        f"/graphql?variables=("
        f"cardSectionTypes:List({card}),jobPostingUrn:{posting_urn},"
        f"includeSecondaryActionsV2:true)"
        f"&queryId=voyagerJobsDashJobPostingDetailSections"
        f".8c361bb81d00d0b85815039e26c73ed8"
        )
    # f".b0928897b71bd00a5a7291755dcd64f0" # what is this number from ????
    # I think this call fails b/c this number is not what the server expects
    data = res.json()
    return data

with open("credentials.json", "r", encoding="utf-8") as f:
    credentials = json.load(f)
    file_path = f"results_{date_string()}.csv"
    Path(file_path).touch()

    if credentials:
        linkedin = Linkedin(credentials["username"], credentials["password"])
        with open(file_path, "w", encoding="utf-8", newline="") as csv_file:
            field_names = [
                "title",
                "technology",
                "money",
                "salary",
                "benefits",
                "industries",
                "posting_id",
                "apply_method",
                "company",
                "seen_at"
            ]
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(field_names)

            found_langs = {}
            found_jobs = []
            for rng in [range(20), range(20, 40), range(40, 60), range(60, 80), range(80, 100)]:
                default_evade()
                for offset in rng:
                    print(f"Page: {offset}")
                    for job in linkedin.search_jobs(
                        keywords="software engineer",
                        experience=["4"],
                        job_type=["F", "C"],
                        location_name="United States",
                        remote=["2"],
                        limit=49,
                        offset=offset,
                    ):
                        job_id = job["entityUrn"].split(":")[3]
                        if job_id not in found_jobs:
                            found_jobs.append(job_id)
                            jd = get_posting(linkedin, job_id)
                            # pprint.pp(jd)
                            salary_insights = unwrap_salary(jd['salaryInsights'])
                            pprint.pp(salary_insights)
                            benies = jd['benefits']
                            pprint.pp(benies)
                            industries = jd['formattedIndustries']
                            pprint.pp(industries)
                            content_source = jd['contentSource']
                            pprint.pp(content_source)
                            job_data = linkedin.get_job(job_id=job_id)
                            description_text = job_data["description"]["text"].lower()
                            title = job_data["title"]
                            posting_id = job_data["jobPostingId"]
                            company = company_name(job_data["companyDetails"])
                            apply_method = apply_url(job_data["applyMethod"])
                            print("Job Found:")
                            pprint.pp(title)
                            pprint.pp(posting_id)

                            langs = [
                                ".net",
                                "android",
                                "angular",
                                "big data",
                                "bigquery",
                                "c#",
                                "c++",
                                "clojerl",
                                "clojure",
                                "cobol",
                                "concurency",
                                "crystal",
                                "dart",
                                "distributed",
                                "django",
                                "elasticsearch",
                                "elixir",
                                "elm",
                                "erlang",
                                "f#",
                                "flask",
                                "flutter",
                                "fortran",
                                "functional",
                                "gleam",
                                "go",
                                "golang",
                                "gql",
                                "graphql",
                                "groovy",
                                "hadoop",
                                "haskell",
                                "hcl",
                                "ios",
                                "java",
                                "javascript",
                                "julia",
                                "kafka",
                                "kotlin",
                                "linux",
                                "lisp",
                                "lua",
                                "mariadb",
                                "mongodb",
                                "mysql",
                                "neo4j",
                                "nim",
                                "node",
                                "node.js",
                                "nodejs",
                                "nosql",
                                "numpy",
                                "objective-c",
                                "ocaml",
                                "pandas",
                                "pascal",
                                "perl",
                                "phoenix",
                                "php",
                                "postgresql",
                                "prolog",
                                "purescript",
                                "python",
                                "pytorch",
                                "racket",
                                "rails",
                                "react",
                                "redis",
                                "redshift",
                                "ruby",
                                "rust",
                                "scala",
                                "scheme",
                                "senior",
                                "smalltalk",
                                "snowflake",
                                "spark",
                                "spring",
                                "swift",
                                "typescript",
                                "vuejs",
                                "wasm",
                                "webasembly",
                                "zig",
                            ]

                            technology = []
                            found = []
                            for lang in langs:
                                reg = rf"\s{re.escape(lang)}[\s,)\.]"
                                maybe_found = re.findall(reg, description_text)
                                if maybe_found != []:
                                    [l, *_] = maybe_found
                                    l_key = l.strip(",").strip(")").strip(".").strip()
                                    tech = consolidate_technology(l_key)
                                    if tech not in found:
                                        found_langs.setdefault(tech, 0)
                                        found_langs[tech] += 1
                                        technology.append(tech)
                                        found.append(tech)
                                        print(f"{tech}: {found_langs[tech]}")

                            MONEY = r"\$[\d|,|k]+"
                            money_found = re.findall(MONEY, description_text)
                            xs = list(map(
                                lambda s: Decimal(re.sub(
                                    r"[^\d.]",
                                    "",
                                    s.replace("k", ",000"))),
                                money_found))
                            xs.sort(reverse=True)
                            mf_dec = list(map(str, xs))

                            csv_writer.writerow(
                                [
                                    title,
                                    str(technology),
                                    str(mf_dec),
                                    str(salary_insights),
                                    str(benies),
                                    str(industries),
                                    posting_id,
                                    str(apply_method),
                                    str(company),
                                    date_string(),
                                ]
                            )

            sorted_langs = dict(sorted(found_langs.items(), key=lambda x: x[1], reverse=True))
            pprint.pp(sorted_langs)
            print(f"Total: {len(found_jobs)}")
