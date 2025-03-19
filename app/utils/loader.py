from typing import List, Tuple, Dict

from . import fs_utils


def load_prompt(step_name: str) -> Tuple[str, List[Tuple[str, str]]]:
    FEW_SHOT_INFO = fs_utils.read_json('./assets/dev_corpus/few_shot_info.json')

    few_shots = []
    system_prompt = fs_utils.read_file(f'./assets/prompts/{FEW_SHOT_INFO[step_name]["step"]}.md')
    for folder in FEW_SHOT_INFO[step_name]['shots']:
        _input = fs_utils.read_file(f'./assets/dev_corpus/{folder}/{FEW_SHOT_INFO[step_name]["prev_step"]}.md')
        _output = fs_utils.read_file(f'./assets/dev_corpus/{folder}/{FEW_SHOT_INFO[step_name]["step"]}.md')
        few_shots.append((_input, _output))
    return system_prompt, few_shots


def load_connectives() -> List[str]:
    hard_connectives = [c.lower() for c in fs_utils.read_file('./assets/hard_connectives.txt').split('\n')]
    hard_connectives = [c + "\\b" for c in hard_connectives if (not c.endswith("*")) or (not c.endswith("]"))]
    hard_connectives = [c.replace("a\\w*", "(a|al|allo|alla|ai|agli|alle|all')\\b") for c in hard_connectives]
    hard_connectives = [c.replace("d\\w*", "(di|del|dello|dell'|della|dei|degli|delle|dal|dallo|dall'|dalla|dai|dagli|dalle')\\b") for c in hard_connectives]
    return hard_connectives