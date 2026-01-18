from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()
model=ChatAnthropic(model='claude-sonnet-4-5-20250929')

reult=model.invoke('What si the capital of india')
print(reult.content)