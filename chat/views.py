from django.shortcuts import render, redirect
from django.views.generic import CreateView
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from chat.forms import MessageForm
from chat.models import Chat, Message
from chatApp.settings import OPENAI_API_KEY


# Create your views here.


class CreateChatView(CreateView):
    model = Chat
    form_class = MessageForm
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are world class support assistant."),
                ("user", "{input}")
            ])

            output_parser = StrOutputParser()
            chain = prompt | llm | output_parser
            response = chain.invoke({"input": content})
            user = request.user
            message = Message(name=content, response=response, user=user)
            message.messages.add(message)
            message.messages.name = message.content
            message.save()
        return redirect('index')

    def get_context_data(self, **kwargs):
        chats = Chat.objects.filter(message__user_id=self.request.user.id)
        context = super().get_context_data(**kwargs)
        context['chats'] = chats
        return context
