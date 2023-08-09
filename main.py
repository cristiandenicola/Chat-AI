import functions
from colorama import init, Fore, Style

def chat_bot():
    knowledge_base: dict = functions.load_knowledge_base('knowledge.json')

    while True:
        user_input: str = input(Fore.LIGHTBLUE_EX +'You: ' + Style.RESET_ALL)

        if user_input.lower() == 'quit':
            break
        
        best_match: str | None = functions.find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]], knowledge_base)
        #implementare ricerca anche sulle keywords

        if best_match:
            answer: str = functions.get_answer_for_question(best_match, knowledge_base)
            print(f'{Fore.LIGHTRED_EX}Bot:{Style.RESET_ALL} {answer}')
        else:
            print(f'{Fore.LIGHTRED_EX}Bot:{Style.RESET_ALL} I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                #estrazione keywords
                #traduzione keywords
                #ricerca sinonimi keyws in eng
                #traduzione sin eng in ita
                #salvataggio
                print()

if __name__ == '__main__':
    init(autoreset=True)
    chat_bot()
