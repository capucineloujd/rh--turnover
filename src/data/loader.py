from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data_raw"


def load_raw_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sirh = pd.read_csv(DATA_DIR / "extrait_sirh.csv")
    df_eval = pd.read_csv(DATA_DIR / "extrait_eval.csv")
    sondage = pd.read_csv(DATA_DIR / "extrait_sondage.csv")
    return sirh, df_eval, sondage


def load_data() -> pd.DataFrame:
    sirh, df_eval, sondage = load_raw_data()

    df_eval["id_employee"] = df_eval["eval_number"].apply(lambda x: int(x.replace("E_", "")))
    sondage["id_employee"] = sondage["code_sondage"].astype(int)

    data = (
        sirh
        .merge(df_eval, on="id_employee", how="inner")
        .merge(sondage, on="id_employee", how="inner")
    )
    return data
