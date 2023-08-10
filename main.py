import functions
from colorama import init, Fore, Style

def chat_bot():
    knowledge_base: dict = functions.load_knowledge_base('knowledge.json')

    while True:
        user_input: str = input(Fore.LIGHTBLUE_EX +'You: ' + Style.RESET_ALL)
        input_eng = functions.translate_to_eng(user_input)

        if input_eng.lower() == 'quit':
            print(f'{Fore.LIGHTRED_EX}ChatAI:{Style.RESET_ALL} Goodbye')
            break
        response = functions.generate_answer(input_eng)
        print(f'{Fore.LIGHTRED_EX}ChatAI:{Style.RESET_ALL} {response}')

if __name__ == '__main__':
    init(autoreset=True)
    chat_bot()
