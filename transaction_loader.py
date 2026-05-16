import pandas as pd

RELEVANT_COLUMNS = [
        "Action", "Time", "Ticker", "No. of shares",
        "Price / share", "Currency (Price / share)", "Withholding tax",
    ]

RELEVANT_ACTIONS = [
        "Market buy", "Limit buy", "Market sell", "Limit sell",
        "Dividend (Dividend)",
    ]

def load_transactions(paths: list[str]) -> pd.DataFrame:
        dfs = [pd.read_csv(p) for p in paths]
        df = pd.concat(dfs)
        df = df[df["Action"].isin(RELEVANT_ACTIONS)]
        df = df.reset_index(drop=True)
        df = df[[c for c in RELEVANT_COLUMNS if c in df.columns]]
        return df