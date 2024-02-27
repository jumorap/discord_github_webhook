import json
import re

from flask import request
from flask import Flask

from discord_webhook import DiscordWebhook, DiscordEmbed

import random


app=Flask(__name__)

phrases = ["Mergeando PRs es como ordenar una pizza, siempre hay sorpresas.", "¿Revisar mi propio PR? Eso es como intentar autocriticarme en el espejo.", "Cuando me piden hacer un PR pequeño, es como pedirme que elija solo un dulce de la tienda.", "PR aprobado sin comentarios es más raro que encontrar papel higiénico al inicio de la pandemia.", "Cada vez que hago un PR, es un episodio nuevo de 'Esperanzas y Desilusiones'.", "Hacer PRs es mi forma de socializar. Sí, estoy disponible para fiestas.", "PRs sin conflictos son como los fantasmas, todos creen hasta que les toca ver uno.", "Mi PR es como una novela, largo y con muchos giros inesperados.", "La vida es corta, pero a veces los PRs no lo son.", "Hacer un PR sin revisión de código es como un día sin café, simplemente no funciona.", "Un PR bien hecho es como una buena broma, necesita el timing perfecto.", "Los PRs son como las citas a ciegas, nunca sabes con qué te vas a encontrar.", "Mergeando un PR sin testear es como saltar en bungee sin cuerda. Aventurero pero no recomendable.", "Enviar un PR es mi momento 'suelta el micrófono' del día.", "Resolver conflictos en PRs es como hacer malabares con cuchillos, un arte peligroso pero impresionante.", "Los PRs son como las cebollas, tienen capas y a veces te hacen llorar.", "Revisar PRs es como buscar el santo grial, una misión épica.", "Enviar un PR es declarar 'aquí estuve yo', con código en vez de graffiti.", "Los PRs son como el clima, siempre cambiando y a veces tormentosos.", "Hacer un PR es como lanzar un mensaje en una botella al océano digital.", "Un PR sin conflicto es como un día sin emails. Teóricamente posible, pero altamente improbable.", "Crear un PR es como hacer magia: conviertes café en código.", "Los PRs son como las películas de misterio, nunca sabes cómo van a terminar.", "Un buen PR es como un buen chiste, si tienes que explicarlo mucho, algo falló.", "Hacer un PR es mi versión de enviar una carta a Santa. Esperanzas altas, resultados inciertos.", "Los PRs son como los gatos, tienen su propia personalidad y no siempre cooperan.", "Enviar un PR es como lanzarse en paracaídas. Esperas que todo se abra correctamente.", "Revisar PRs es como ir a cazar tesoros. A veces encuentras oro, a veces solo calcetines viejos.", "PRs: porque compartir código debería ser tan emocionante como compartir chismes.", "Los PRs son como las citas: primero impresionas, luego negocias condiciones.", "Merge de PR: el momento en que tu código pasa de ser un héroe a ser parte del equipo.", "Los PRs son el reality show del desarrollo de software. Drama, acción y a veces, romance.", "Un PR exitoso es como un buen café: satisfactorio, necesario y motivo para celebrar.", "Hacer un PR es como proponer matrimonio: esperas un sí, pero preparado para cualquier cosa.", "PRs son como puzzles: divertidos hasta que faltan piezas o no encajan.", "Los PRs son como los sueños, grandes hasta que el revisor los trae de vuelta a la realidad.", "Enviar un PR es como enviar un hijo a la escuela: esperas lo mejor, pero te preparas para las llamadas.", "PRs: la mezcla perfecta entre esperanza, terror y el ocasional meme de gato.", "Resolver conflictos de PR es como mediar en una discusión de pareja: delicado y siempre buscando el compromiso.", "Los PRs son como las olas del mar: vienen, causan un poco de caos y luego se calman."]
blacklist = []
pr_threads = {

}


@app.route('/github', methods=['POST'])
def webhook_message():
    url_webhook = request.args.get('webhook_url')
    req_json = request.json

    if request.headers['X-Github-Event']=='pull_request' and req_json["action"] == "opened":

        branch_name = req_json["pull_request"]["head"]["ref"]
        url_pr = req_json["pull_request"]["html_url"]
        description_pr = req_json["pull_request"]["body"]
        user_pr = req_json["pull_request"]["user"]["login"]
        avatar_url = req_json["pull_request"]["user"]["avatar_url"]
        pick_phrase = random.choice(phrases)

        if url_pr in blacklist:
            return "success"

        blacklist.append(url_pr)

        thread_name_return = f"{branch_name} {url_pr}"
        description_return = f"**Descripción:** {description_pr} \n\n *{pick_phrase}*"

        embed_content = DiscordEmbed(url=url_pr, title=user_pr, description=description_return, color="03b2f8")
        webhook = DiscordWebhook(url=url_webhook, thread_name=thread_name_return, username="Captain PR", avatar_url=avatar_url)

        webhook.add_embed(embed_content)
        wh = webhook.execute()
        pr_threads[url_pr] = json.loads(wh.content.decode("utf-8"))["id"]


    elif request.headers['X-Github-Event']=='issue_comment':
        url_pr_comment = req_json["issue"]["comments_url"]
        url_pr = req_json["issue"]["html_url"]
        description_pr = req_json["comment"]["body"]
        avatar_url = req_json["comment"]["user"]["avatar_url"]
        author = req_json["comment"]["user"]["login"]
        id_thread_return = pr_threads[url_pr]
        author_return = f"**{author}** says:"

        if description_pr.find("<@") != -1:
            user_mentions = re.findall(r'<@!?\d{18}>', description_pr)[0]

        embed_content = DiscordEmbed(url=url_pr_comment, title=author_return, description=description_pr, color="03b2f8")
        webhook = DiscordWebhook(url=url_webhook, thread_id=int(id_thread_return), username="Captain PR - Comments", avatar_url=avatar_url, content=user_mentions)

        webhook.add_embed(embed_content)
        webhook.execute()

    return "success"


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5012, debug=True)
