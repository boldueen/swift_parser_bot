from rabbit_consumer import Consumer
consumer = Consumer()


def main():
    consumer.start_consuming()


if __name__ == '__main__':
    main()
