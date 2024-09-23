from langchain_groq import ChatGroq # type: ignore
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import MessagesPlaceholder,ChatPromptTemplate
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from chat.models import Message, CustomGPT
from chat.serializers import MessageSerializer

llm = ChatGroq(api_key= os.getenv('GROQ_API_KEY'), model = 'llama3-70b-8192')


class Chat:
    
    def __init__(self, gpt:CustomGPT, user_id: str):
        self.gpt = gpt
        self.gpt_name = gpt.name
        self.system_prompt = gpt.system_prompt
        self.user_id = user_id
        self.message_history = self.get_session_history()
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        self.question_answer_chain = self.qa_prompt | llm | StrOutputParser()

        self.conversational_rag_chain = RunnableWithMessageHistory(
            self.question_answer_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
    def get_session_history(self, id:str = 'default') -> BaseChatMessageHistory:
        message_history = SQLChatMessageHistory(session_id=self.gpt_name, connection_string=os.getenv('MEMORY_DATABASE_URL'), table_name = self.user_id)
        return message_history
    
    def add_messages_to_table(self, user_message: str, ai_message: str):
        message = Message(custom_gpt = self.gpt, user_id = self.user_id, user_message = user_message, ai_message = ai_message)
        message.save()
        return message
    
    
    def get_response(self, input: str) -> str:
        response = self.conversational_rag_chain.invoke({"input": input},
                      config={
                          "configurable": {"session_id": 'default'}
                      })
        self.message_history.add_user_message(input)
        self.message_history.add_ai_message(response)
        message = self.add_messages_to_table(input, response)
        message_data = MessageSerializer(message).data
        return message_data