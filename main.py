from pii_mask import mask
from read_queue import read
from ingest import push_postgres


def main():
    df = read("http://localhost:4566/000000000000/login-queue", "login-queue")
    masked_df = mask(df)
    push_postgres(masked_df)


if __name__ == '__main__':
    main()
