import matplotlib.pyplot as plt

def load_data_threads(filename):
    threads = []
    times = []
    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split()
            threads.append(int(data[0]))
            times.append(float(data[1]))
    return threads, times

def load_data_pages(filename):
    pages = []
    times_seq = []
    times_par = []
    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split()
            pages.append(int(data[0]))
            times_seq.append(float(data[1]))
            times_par.append(float(data[2]))

    return pages, times_seq, times_par

def plot_threads(threads, times):
    plt.figure(figsize=(10, 6))
    plt.plot(threads, times, marker='o', linestyle='-', color='b')

    plt.title('Зависимость времени от числа потоков')
    plt.xlabel('Число потоков')
    plt.ylabel('Время (секунды)')
    plt.grid(True)

    plt.savefig('threads.png')


def plot_pages(pages, times_seq, times_par):
    plt.figure(figsize=(10, 6))
    plt.plot(pages, times_seq, marker='o', linestyle='-', color='b', label="1 поток")
    plt.plot(pages, times_par, marker='o', linestyle='-', color='r', label="12 потоков")

    plt.title('Зависимость времени от числа страниц')
    plt.xlabel('Число страниц (шт)')
    plt.ylabel('Время, (секунды)')
    plt.legend(loc='best')
    plt.grid(True)

    plt.savefig('pages.png')



if __name__ == '__main__':
    filename_threads = '/home/vasiliy/Documents/study/3rd_course/1st_sem/AA/lab_04/data/res_threads.txt'
    filename_pages = '/home/vasiliy/Documents/study/3rd_course/1st_sem/AA/lab_04/data/res_pages.txt'
    threads, times = load_data_threads(filename_threads)
    pages, times_seq, times_par = load_data_pages(filename_pages)

    plot_threads(threads, times)
    plot_pages(pages, times_seq, times_par)