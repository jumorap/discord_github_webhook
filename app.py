from flask import request
from flask import Flask

import services.pr_request as pr_request
import services.pr_issued_messages as pr_issued_messages
import services.pr_merge as pr_merge
import services.pr_reject as pr_reject
import phrases

import json


app=Flask(__name__)

# Mutables
blacklist: list = []
pr_threads: dict = {}
sha_pr_threads: dict = {}
already_merged: list = []


@app.route('/github', methods=['POST'])
def webhook_message() -> str:
    """
    This function is the main function that will be called when a webhook is triggered with a POST request.
    Format: URL:PORT/github?webhook_url=URL_FORUM_WORKFLOW
    :return: str - success
    """
    url_webhook = request.args.get('webhook_url')
    req_json = request.json
    github_type_request = request.headers['X-Github-Event']

    if req_json is None:
        print("No JSON found")
        return "success"

    # PR opened
    if "action" in req_json and github_type_request == 'pull_request' and req_json["action"] == "opened":
        sha_code = req_json["pull_request"]["base"]["sha"]
        url_pr = req_json["pull_request"]["html_url"]

        if url_pr in blacklist:
            return "success"

        wh = pr_request.send_pr_request(
            req_json,
            url_webhook,
            url_pr,
            phrases.phrases_pr
        )

        blacklist.append(url_pr)
        sha_pr_threads[sha_code] = url_pr
        pr_threads[url_pr] = json.loads(wh.content.decode("utf-8"))["id"]

    # PR comments
    elif github_type_request == 'issue_comment':
        pr_issued_messages.post_message_from_github(
            req_json,
            url_webhook,
            pr_threads
        )

    # PR merged
    elif github_type_request == 'push' and "pusher" in req_json and "before" in req_json:
        before_sha_code = req_json["before"]

        if before_sha_code not in sha_pr_threads:
            return "success"

        url_pr = sha_pr_threads[before_sha_code]
        thread_id = pr_threads[url_pr]

        pr_merge.send_pr_merge(
            req_json,
            url_webhook,
            url_pr,
            thread_id,
            phrases.phrases_merged
        )

        already_merged.append(url_pr)

    # PR closed => rejected
    elif github_type_request == 'pull_request' and "action" in req_json and req_json["action"] == "closed" and req_json["pull_request"]["merged"] is False:
        url_pr = req_json["pull_request"]["html_url"]
        thread_id = pr_threads[url_pr]

        if url_pr in already_merged:
            return "success"

        pr_reject.send_pr_reject(
            req_json,
            url_webhook,
            url_pr,
            thread_id,
            phrases.phrases_closed
        )

    return "success"


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5012, debug=True)
