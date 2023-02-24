import time


def main():
    print('backend service starting')
    while True:
        time.sleep(2)
        print('backend service running')


if __name__ == "__main__":
    main()
