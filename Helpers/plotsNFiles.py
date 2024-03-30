from matplotlib import pyplot as plt


def make_plot(values: list, file_name: str, title: str, y_scale: str = 'linear') -> None:
    plt.plot(values)
    plt.yscale(y_scale)
    plt.title(title)
    plt.xlabel('Population')
    plt.ylabel(file_name)
    plt.savefig(f'{file_name}.png')
    plt.figure()


def save_to_file(values: list, file_name: str) -> None:
    with open(f'./{file_name}.txt', 'w') as f:
        i = 1
        for value in values:
            f.write(f'epoch {i}: {value}\n')
            i += 1
