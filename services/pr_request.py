from discord_webhook import DiscordWebhook, DiscordEmbed

import random
import requests


def send_pr_request(req_json: dict, url_webhook: str, url_pr: str, phrases: list) -> "requests.Response":
    """
    Send a message to a discord channel with the information of a pull request and a random phrase
    :param req_json: The GitHub request got from the POST request to the current webhook
    :param url_webhook: The URL of the discord webhook
    :param url_pr: The URL of the pull request
    :param phrases: A list of phrases to be used in the message
    :return: The response of the webhook that contains all the information of the Discord message
    """
    branch_name = req_json["pull_request"]["head"]["ref"]
    description_pr = req_json["pull_request"]["body"]
    user_pr = req_json["pull_request"]["user"]["login"]
    avatar_url = req_json["pull_request"]["user"]["avatar_url"]
    pick_phrase = random.choice(phrases)

    thread_name_return = f"{branch_name} {url_pr}"
    notion_link = f"[**Notion task:** {branch_name}](https://www.notion.so/{branch_name})"
    description_return = f"**Overview:** {description_pr} \n\n {notion_link} \n\n *{pick_phrase}*"

    embed_content = DiscordEmbed(url=url_pr, title=user_pr, description=description_return, color="03b2f8")
    webhook = DiscordWebhook(url=url_webhook, thread_name=thread_name_return, username="Captain PR",
                                 avatar_url=avatar_url)

    webhook.add_embed(embed_content)

    return webhook.execute()
