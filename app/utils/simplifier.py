import os
import re
from typing import List

from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.models.SimplificationResponse import SimplificationProgress
from app.utils import loader

class AbstractSimplifier:
    def __init__(self, prev_step: str, step: str):
        self.prev_step = prev_step
        self.step = step

        self.openai = ChatOpenAI(base_url=os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1"), api_key=SecretStr(os.getenv("OPENAI_API_KEY", "")),
                                 model="gpt-4o-mini",
                                 max_tokens=4095,
                                 temperature=0.1, top_p=0.2,
                                 frequency_penalty=0.0, presence_penalty=0.0)
        self.sempl_it = ChatOpenAI(base_url=os.getenv("SEMPL_IT_ENDPOINT", "http://localhost:9000/v1"), api_key=SecretStr(os.getenv("SEMPL_IT_API_KEY", "")),
                                   model=self.step,
                                   max_tokens=4095,
                                   temperature=0.1, top_p=0.2,
                                   frequency_penalty=0.0, presence_penalty=0.0)

    def simplify(self, _progress: SimplificationProgress):
        print(f"Running {self.step} simplification")

        text_to_simplify = _progress[self.prev_step]
        prompt = self.prompt(_progress["mode"], text_to_simplify)

        if _progress["mode"] == "openai":
            text_simplified = self.openai.invoke(prompt).content
        else:
            text_simplified = self.sempl_it.invoke(prompt).content

        _progress.update({self.step: self.postprocess_output(text_simplified)})
        return _progress

    def prompt(self, mode: str, text: str) -> List[BaseMessage]:
        system_prompt, few_shots = loader.load_prompt(self.step)

        messages = [SystemMessage(system_prompt)]
        if mode == "openai":
            for example in few_shots:
                messages.append(HumanMessage(self.process_user_input(example[0])))
                messages.append(AIMessage(example[1]))

        messages.append(HumanMessage(self.process_user_input(text)))
        return messages

    def process_user_input(self, user_input: str) -> str:
        return user_input

    def postprocess_output(self, output: str) -> str:
        output = output.replace('**', '')
        return '\n'.join([x.rstrip() for x in output.split('\n')])


class Proofreader(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="original", step="proofreading")


class LexNormalizer(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="proofreading", step="lex")


class ConnectivesSimplifier(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="lex", step="connectives")
        self.connectives = loader.load_connectives()

    def process_user_input(self, user_input: str) -> str:
        connectives_found = []
        for conn in self.connectives:
            results = [m.group() for m in re.finditer(conn, user_input, re.IGNORECASE)]
            connectives_found.extend(results)

        output = "## Testo\n" + user_input + "\n\n## Connettivi\n"
        if len(connectives_found) == 0:
            output += "[Nessuno]"
        else:
            for c in connectives_found:
                output += f"- {c}\n"
        return output

class ExpressionsSimplifier(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="connectives", step="expressions")

class SentenceSplitter(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="expressions", step="sentence_splitter")

class NominalizationsSimplifier(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="sentence_splitter", step="nominalizations")

class VerbsSimplifier(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="nominalizations", step="verbs")

class SentenceReorganizer(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="verbs", step="sentence_reorganizer")