import pandas as pd
import matplotlib.pyplot as plt


def scrap_year_file(year):
    names = pd.read_csv('babynames/yob' + str(year) + '.txt',
                        sep=',',
                        header=None,
                        names=['name', 'sex', 'number'])
    names['sex'] = names['sex'].str.replace('M', 'Male', regex=False).str.replace('F', 'Female', regex=False)

    names['year'] = year

    return names


def build_single_file():
    years_list = []
    for year in range(2010, 1879, -1):
        years_list.append(scrap_year_file(year))

    names = pd.concat(years_list, axis='index', copy=False, ignore_index=True)

    return names


def plot_birth_stats(names):
    total = names.groupby(['sex', 'year']).sum().unstack().T
    total.plot.bar(stacked=True)
    plt.show()


def plot_popular_names(names):
    total = names.groupby(['name']).sum().sort_values('number', ascending=False)['number'][:20]
    total.plot.bar()
    plt.show()


def plot_decade_popular_names(names):
    total = names.groupby(['sex', 'year', 'name']).sum().unstack()

    decade_stat = []
    for i in range(1880, 2010, 13):
        male = total.loc['Male'].loc[i:i+13].sum()
        female = total.loc['Female'].loc[i:i + 13].sum()
        m_name = male[male == male.max()].index[0][1]
        f_name = female[female == female.max()].index[0][1]
        if m_name not in decade_stat:
            decade_stat.append(m_name)
        if f_name not in decade_stat:
            decade_stat.append(f_name)

    total = names.groupby(['name', 'year']).sum().unstack()
    years = list(range(1880, 2011))
    for name in decade_stat:
        plt.plot(years, total.loc[name], label=name)

    plt.legend()
    plt.show()


def plot_half_names(names):
    total = names.groupby(['year', 'name']).sum().unstack()

    names_number = []
    for year in range(1880, 2011):
        half_year = total.loc[year].sum() / 2
        sorted = total.loc[year].sort_values(ascending=False)
        for i in range(1, len(total.loc[year])):
            s = sorted[:i].sum()
            if s >= half_year:
                names_number.append(i)
                break

    years = list(range(1880, 2011))
    plt.plot(years, names_number)
    plt.title('name variation through years')
    plt.xlabel('years')
    plt.ylabel('number of most usable names')
    plt.show()


def plot_letter_distr(names, position):     #position should be 'first' or 'last'
    index = None
    if position == 'first':
        index = 0
    elif position == 'last':
        index = -1
    else:
        raise ValueError('position should be "first" or "last" only')

    letters = list('abcdefghijklmnopqrstuvwxyz')

    ys = []
    for i in range(1900, 2000, 25):
        y = names[names['year'] == i]
        y[position] = y['name'].str.lower().str[index]
        gr = y.groupby([position]).sum()['number']
        for l in letters:
            if l not in gr:
                gr = gr.append(pd.Series({l: 0}), )
        gr.sort_index(inplace=True)
        gr = gr / gr.sum()
        ys.append(gr)

    for i in range(len(ys)):
       plt.plot(letters, ys[i], label=str(1900 + i * 25))
    plt.xlabel(position + ' letter')
    plt.ylabel('frequency')
    plt.legend()
    plt.show()


def plot_famous(names):
    total = names.groupby(['name', 'year']).sum().unstack()

    years = list(range(1880, 2011))
    # fig, ax = plt.subplots()
    plt.plot(years, total.loc['Luke'])
    plt.title('frequency of name "Luke"')
    plt.xlabel('years')
    plt.annotate('star wars ep. 4 movie',
                 xy=(1977, 1100),
                 xytext=(1920, 2000),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('star wars ep. 1 movie',
                 xy=(1999, 5700),
                 xytext=(1940, 8000),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.show()

    plt.plot(years, total.loc['Forrest'])
    plt.title('frequency of name "Forrest"')
    plt.xlabel('years')
    plt.annotate('Forrest Gump movie',
                 xy=(1994, 1350),
                 xytext=(1920, 1000),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.show()


if __name__ == '__main__':
    names = build_single_file()

    plot_birth_stats(names)

    plot_popular_names(names)

    plot_decade_popular_names(names)

    plot_half_names(names)

    plot_letter_distr(names, 'first')

    plot_letter_distr(names, 'last')

    plot_famous(names)

