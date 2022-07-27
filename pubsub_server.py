from whatsapp.adapters.middleware import PubSubProxy


def main():
    PubSubProxy().start()


if __name__ == '__main__':
    main()
