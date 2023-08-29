from rabbit_consumer import Consumer


def main():
    consumer = Consumer()
    consumer.start_consuming()


if __name__ == '__main__':
    main()
