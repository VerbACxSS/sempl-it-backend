from langgraph.constants import START, END
from langgraph.graph import StateGraph

from ..models.SimplificationResponse import SimplificationProgress
from ..utils.simplifier import Proofreader, LexNormalizer, ConnectivesSimplifier, \
    ExpressionsSimplifier, SentenceSplitter, NominalizationsSimplifier, VerbsSimplifier, SentenceReorganizer


class SimplificationService:
    def __init__(self):
        self.proofreader = Proofreader()
        self.lex_normalizer = LexNormalizer()
        self.connectives_simplifier = ConnectivesSimplifier()
        self.expression_simplifier = ExpressionsSimplifier()
        self.sentences_simplifier = SentenceSplitter()
        self.nominalizations_simplifier = NominalizationsSimplifier()
        self.verbs_simplifier = VerbsSimplifier()
        self.sentence_reorganizer = SentenceReorganizer()

        # Build workflow
        workflow = StateGraph(SimplificationProgress)

        # Add nodes
        workflow.add_node("proofreading_node", self.proofreader.simplify)
        workflow.add_node("lex_node", self.lex_normalizer.simplify)
        workflow.add_node("connectives_node", self.connectives_simplifier.simplify)
        workflow.add_node("expressions_node", self.expression_simplifier.simplify)
        workflow.add_node("sentence_splitter_node", self.sentences_simplifier.simplify)
        workflow.add_node("nominalizations_node", self.nominalizations_simplifier.simplify)
        workflow.add_node("verbs_node", self.verbs_simplifier.simplify)
        workflow.add_node("sentence_reorganizer_node", self.sentence_reorganizer.simplify)

        # Add edges
        workflow.add_edge(START, "proofreading_node")
        workflow.add_edge("proofreading_node", "lex_node")
        workflow.add_edge("lex_node", "connectives_node")
        workflow.add_edge("connectives_node", "expressions_node")
        workflow.add_edge("expressions_node", "sentence_splitter_node")
        workflow.add_edge("sentence_splitter_node", "nominalizations_node")
        workflow.add_edge("nominalizations_node", "verbs_node")
        workflow.add_edge("verbs_node", "sentence_reorganizer_node")
        workflow.add_edge("sentence_reorganizer_node", END)

        # Compile workflow
        self.chain = workflow.compile()

    def simplify(self, text_to_simplify: str, mode: str) -> SimplificationProgress:
        progress = SimplificationProgress()
        progress.mode = mode
        progress.original = text_to_simplify
        return self.chain.invoke(progress)
