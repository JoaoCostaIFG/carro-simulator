#!/usr/bin/env python3

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


from carro.Carro import Carro


def doPlot(df, title, outFile):
    plt.figure(figsize=(40, 20), dpi=300)
    # speeds
    ax = df.plot(
        x="Total elapsed time (s)",
        y="Real vehicle speed (km/h)",
        legend=False,
        color="b",
    )
    df.plot(
        x="Total elapsed time (s)",
        y="Vehicle speed (km/h)",
        ax=ax,
        legend=False,
        color="c",
        alpha=0.4,
    )
    plt.title(title)
    # accelerations
    ax2 = ax.twinx()
    df.plot(
        x="Total elapsed time (s)",
        y="Real acceleration (m/s^2)",
        ax=ax2,
        legend=False,
        color="r",
    )
    df.plot(
        x="Total elapsed time (s)",
        y="Acceleration (m/s^2)",
        ax=ax2,
        legend=False,
        color="orange",
        alpha=0.4,
    )
    ax.figure.legend()
    # plt.show()
    plt.savefig("out/" + outFile)


def main(filename, title):
    c: Carro = Carro()
    df = pd.read_csv(filename, sep=";")

    speeds = []
    accs = []
    c.parkingBrake = False
    for _, row in df.iterrows():
        wantedAcc = row["Acceleration (m/s^2)"]
        c.setAcceleration(wantedAcc)
        c.update(1)  #  sec elapsed
        # save data
        speeds.append(c.speed)
        accs.append(c.acceleration)
    df["Real vehicle speed (km/h)"] = speeds
    df["Real acceleration (m/s^2)"] = accs

    doPlot(df, title, title + ".png")
    for phase in df["Phase"].unique():
        doPlot(df[df["Phase"] == phase], f"{title}-{phase}", f"{title}_{phase}.png")


if __name__ == "__main__":
    main("wltp-class1.csv", "WLTP Class 1")
    main("wltp-class3.csv", "WLTP Class 3")
