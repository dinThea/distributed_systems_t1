from whatsapp.main.prompt import TopicPrompt


def main():

    prompt = TopicPrompt()
    try:
        prompt.cmdloop()
    except KeyboardInterrupt:
        print("Interrupted")

    del prompt._subscriber


if __name__ == '__main__':
    main()
