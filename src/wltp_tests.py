#!/usr/bin/env python3

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


from carro.Carro import Carro


def doPlot(df, title, outFile):
    plt.figure(figsize=(25, 15), dpi=300)
    plt.title(title)
    # speeds
    ax = sb.lineplot(
        data=df,
        x="Total elapsed time (s)",
        y="Real vehicle speed (km/h)",
        color="b",
    )
    sb.lineplot(
        data=df,
        x="Total elapsed time (s)",
        y="Vehicle speed (km/h)",
        ax=ax,
        color="c",
        alpha=0.4,
    )
    # accelerations
    ax2 = ax.twinx()
    sb.lineplot(
        data=df,
        x="Total elapsed time (s)",
        y="Real acceleration (m/s^2)",
        ax=ax2,
        color="r",
    )
    sb.lineplot(
        data=df,
        x="Total elapsed time (s)",
        y="Acceleration (m/s^2)",
        ax=ax2,
        color="orange",
        alpha=0.4,
    )
    plt.legend(
        handles=[
            mlines.Line2D([], [], color="blue", label="Real vehicle speed (km/h)"),
            mlines.Line2D([], [], color="cyan", label="Intended vehicle speed (km/h)"),
            mlines.Line2D([], [], color="red", label="Real acceleration (m/s^2)"),
            mlines.Line2D(
                [], [], color="orange", label="Intended acceleration (m/s^2)"
            ),
        ]
    )
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

    fileTitle = title.replace(" ", "")
    doPlot(df, title, fileTitle + ".png")
    for phase in df["Phase"].unique():
        doPlot(
            df[df["Phase"] == phase],
            f"{title} - {phase}",
            f"{fileTitle}_{phase}.png",
        )


if __name__ == "__main__":
    main("wltp-class1.csv", "WLTP Class 1")
    main("wltp-class3.csv", "WLTP Class 3")
