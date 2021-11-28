import pandas as pd


def main():
    with open("data/taxi_2021-06.csv", "r") as csvfile:
        df = pd.read_csv(csvfile)

    df.pickup_datetime = pd.to_datetime(df.pickup_datetime)
    group = df.groupby(pd.Grouper(freq='1min', key='pickup_datetime'))
    taxi_count_df = group.agg({"dropoff_datetime": "count", 'passenger_count': 'sum'})
    taxi_count_df = taxi_count_df.rename(columns={"dropoff_datetime": "taxi_count"})

    with open("data/taxi_count_2021-06.csv", "w") as csvfile:
        taxi_count_df.to_csv(csvfile)


if __name__ == '__main__':
    main()
