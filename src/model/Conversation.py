import os
import json
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

DATA_DIR = ".data/conversation"

class Message(BaseModel):
    type: Optional[str] = "text"
    role: str
    content: str


class Conversation(BaseModel):
    id: str = str(uuid4())
    title: Optional[str] = "New Conversation"
    messages: list[Message]


class ChatController:
    
    @property
    def conversations(self):
        if not self._conversations:
            self._conversations = self.load()
        return self._conversations
    
    @conversations.setter
    def conversations(self, value):
        self._conversations = value
    
    def load(self):
        data: list[Conversation] = []
        for file in os.listdir(DATA_DIR):
            if not file.endswith(".json"): continue
            with open(os.path.join(DATA_DIR, file), "r") as f:
                conversation_data = json.load(f)
                data.append(Conversation(**conversation_data))
        return data

    
    def create_conversation(self, title = None) -> Conversation:
        conversation = Conversation(title=title, messages=[])
        self.conversations.append(conversation)
        with open(DATA_DIR + f"/{conversation.id}.json", "w") as f:
            json.dump(conversation.model_dump(), f, indent=4)
        return conversation


    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        for conversation in self.conversations:
            if conversation.id == conversation_id:
                return conversation
        return None

    
    def add_message(self, conversation_id: str, message: Message):
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.messages.append(message)
            with open(DATA_DIR + f"/{conversation.id}.json", "w") as f:
                json.dump(conversation.model_dump(), f, indent=4)

