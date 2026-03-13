import matplotlib.pyplot as plt


def plot_sorted_bar_chart(
    filenames: list[str],
    values: list[int],
    title: str,
    output_path: str
):
    # сортировка по убыванию
    sorted_data = sorted(
        zip(filenames, values),
        key=lambda x: x[1],
        reverse=True
    )

    sorted_filenames, sorted_values = zip(*sorted_data)

    plt.figure(figsize=(12, 6))

    bars = plt.bar(
        sorted_filenames,
        sorted_values,
        color="#ff69b4"
    )

    plt.title(title)
    plt.ylabel("Количество слов")
    plt.xticks(rotation=45, ha="right")

    # подписи значений
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height * 1.01,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()