from discord_webhook import DiscordWebhook, DiscordEmbed

import re


def post_message_from_github(req_json: dict, url_webhook: str, pr_threads: dict) -> None:
    """
    Send a message got from GitHub to a discord channel picked from the url as id of the thread with the id
    of the thread where the message has to be sent
    :param req_json: The GitHub request got from the POST request to the current webhook
    :param url_webhook: The URL of the discord webhook
    :param pr_threads: A dictionary with the URL of the pull request as key and the id of the thread as value
    :return: None
    """
    url_pr_comment = req_json["issue"]["comments_url"]
    url_pr = req_json["issue"]["html_url"]
    description_pr = req_json["comment"]["body"]
    avatar_url = req_json["comment"]["user"]["avatar_url"]
    author = req_json["comment"]["user"]["login"]
    id_thread_return = pr_threads[url_pr]
    author_return = f"**{author}** says:"
    user_mentions = ""

    if description_pr.find("<@") != -1:
        user_mentions = re.findall(r'<@!?\d{18}>', description_pr)[0]

    embed_content = DiscordEmbed(url=url_pr_comment, title=author_return, description=description_pr, color="ffffff")
    webhook = DiscordWebhook(url=url_webhook, thread_id=int(id_thread_return), username="Captain PR - Comments",
                             avatar_url=avatar_url, content=user_mentions)

    webhook.add_embed(embed_content)
    webhook.execute()
