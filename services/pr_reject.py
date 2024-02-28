from discord_webhook import DiscordWebhook, DiscordEmbed

import random


def send_pr_reject(req_json: dict, url_webhook: str, url_pr: str, thread_id: str, phrases: list) -> None:
    """
    Send a message to a discord channel with the information of a pull request that was merged
    :param req_json: The GitHub request got from the POST request to the current webhook
    :param url_webhook: The URL of the discord webhook
    :param url_pr: The URL of the pull request
    :param thread_id: The ID of the thread where the message has to be sent
    :param phrases: A list of phrases to be picked randomly
    """
    title_merge = "**❌ PR Rejected!**"
    pick_phrase = random.choice(phrases)
    description_return = f"*{pick_phrase}*"
    avatar_url = req_json["pull_request"]["user"]["avatar_url"]

    embed_content = DiscordEmbed(url=url_pr, title=title_merge, description=description_return, color="f92f60")
    webhook = DiscordWebhook(url=url_webhook, thread_id=int(thread_id), username="Captain PR - Comments",
                             avatar_url=avatar_url)

    webhook.add_embed(embed_content)
    webhook.execute()
