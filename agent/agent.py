import os
import json
import requests

from policy import evaluate_policy


GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
GITHUB_RUN_ID = os.environ["GITHUB_RUN_ID"]

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2026-03-10",
}


def get_pending_deployments():
    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_REPOSITORY}/actions/runs/"
        f"{GITHUB_RUN_ID}/pending_deployments"
    )

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()


def review_deployment(environment_id, state, comment):
    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_REPOSITORY}/actions/runs/"
        f"{GITHUB_RUN_ID}/pending_deployments"
    )

    payload = {
        "environment_ids": [environment_id],
        "state": state,
        "comment": comment,
    }

    response = requests.post(
        url,
        headers=HEADERS,
        json=payload,
    )

    response.raise_for_status()

    print(f"Deployment {state} successfully.")


def load_plan():
    with open("plan.json", "r") as file:
        return json.load(file)


def main():

    print("====================================")
    print(" Terraform Deployment Agent")
    print("====================================")

    plan = load_plan()

    decision, reason = evaluate_policy(plan)

    print(f"Decision : {decision}")
    print(f"Reason   : {reason}")

    deployments = get_pending_deployments()

    if not deployments:
        print("No pending deployment found.")
        return

    for deployment in deployments:

        environment = deployment["environment"]

        print(
            f"Environment: {environment['name']}"
        )

        if decision == "APPROVE":

            review_deployment(
                environment["id"],
                "approved",
                reason,
            )

        else:

            review_deployment(
                environment["id"],
                "rejected",
                reason,
            )


if __name__ == "__main__":
    main()