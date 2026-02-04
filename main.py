import discord
import os
import random
import re

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        resposta = self.rolar_dados(message.content)
        if resposta:
            await message.reply(resposta, mention_author=True)

    def rolar_uma_vez(self, mensagem: str):
        mensagem = re.sub(r'\s+', '', mensagem)

        dados = re.findall(r'(\d+)[dD](\d+)', mensagem)
        if not dados:
            return None

        valores = []
        soma = 0

        for qtd, faces in dados:
            qtd = int(qtd)
            faces = int(faces)

            if qtd > 100 or faces > 1000:
                return None

            for _ in range(qtd):
                valor = random.randint(1, faces)
                valores.append(valor)
                soma += valor

        resultado_final = soma

        resto = re.sub(r'(\d+)[dD](\d+)', '', mensagem)
        modificadores = re.findall(r'([\+\-]\d+)', resto)

        for mod in modificadores:
            resultado_final += int(mod)

        return valores, soma, resultado_final

    def rolar_dados(self, mensagem: str):
        mensagem = mensagem.strip()

        # 🔹 Caso com #
        match_hash = re.match(r'^\s*(\d+)\s*#\s*(.+)$', mensagem)
        if match_hash:
            vezes = int(match_hash.group(1))
            expressao = match_hash.group(2)

            if vezes > 20:
                return None

            linhas = []

            for _ in range(vezes):
                resultado = self.rolar_uma_vez(expressao)
                if not resultado:
                    return None

                valores, soma, final = resultado
                linhas.append(f"{valores} = {soma} = {final}")

            return "\n".join(linhas)

        # 🔹 Rolagem normal
        resultado = self.rolar_uma_vez(mensagem)
        if not resultado:
            return None

        valores, soma, final = resultado

        if soma == final:
            return f"{valores} = {soma}"

        return f"{valores} = {soma} = {final}"


intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("Defina a variável de ambiente DISCORD_TOKEN antes de iniciar o bot.")
client.run(token)