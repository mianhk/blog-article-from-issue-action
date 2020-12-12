#! /usr/bin/env python3


import sys
import json
from datetime import datetime
import base64


def main():
    issue_json = base64.b64decode(sys.argv[1]).decode("utf-8")
    user = sys.argv[2]
    issue = json.loads(issue_json)
    print(json.dumps(issue, indent=2))

    if user != issue["user"]["login"] or "BlogPost" not in [
        l["name"] for l in issue["labels"]
    ]:
        print(f"::set-output name=valid::false")
        return

    tags = "\n".join(
        [
            "- " + l["name"][l["name"].find("/") + 1 :]
            for l in issue["labels"]
            if l["name"].startswith("tags/")
        ]
    )
    categories = "\n".join(
        [
            "- " + l["name"][l["name"].find("/") + 1 :]
            for l in issue["labels"]
            if l["name"].startswith("categories/")
        ]
    )
    article = f"""
---
title: '{issue["title"]}'
tags:
{tags}
categories:
{categories}
date: {datetime.fromisoformat(issue["created_at"][:-1]).strftime("%Y-%m-%d %X")}
---

{issue["body"]}
"""
    article_escaped = base64.b64encode(article.encode("utf-8")).decode("utf-8")
    print(article)
    print(f"::set-output name=article::{article_escaped}")
    print(f"::set-output name=valid::true")


if __name__ == "__main__":
    main()
