from cmao.core.state import ConversationState
from cmao.orchestration.loop import step

state = ConversationState()
print(step(state, 'Hello there'))
