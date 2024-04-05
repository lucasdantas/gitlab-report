import pandas as pd


months_pt_br = {
        '2024-01': 'Janeiro', '2024-02': 'Fevereiro', '2024-03': 'Março',
        '2024-04': 'Abril', '2024-05': 'Maio', '2024-06': 'Junho',
        '2024-07': 'Julho', '2024-08': 'Agosto', '2024-09': 'Setembro',
        '2024-10': 'Outubro', '2024-11': 'Novembro', '2024-12': 'Dezembro'
        }


def commit_table(users):
    datas = []

    # Extrair dados relevantes de cada usuário
    for user in users:
        name = user['name']  # Usando o nome do usuário
        user_months = user.get('month_contributions', {})
        for month, details in user_months.items():
            datas.append({
                'name': name,
                'month': month,
                'commits': details['commits'],
                })

    # Preparando os dados
    df = pd.DataFrame(datas)
    df['month'] = pd.to_datetime(df['month'])
    df.sort_values(by=['name', 'month'], inplace=True)
    df['month'] = df['month'].dt.strftime('%Y-%m')

    pivot_df = df.pivot(index='name', columns='month', values='commits').fillna(0)
    pivot_df.columns.name = None
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'name': 'Nome'}, inplace=True)
    pivot_df.rename(columns=months_pt_br, inplace=True)

    # Certificar de converter todas as colunas para inteiros, exceto a coluna de nome
    for col in pivot_df.columns[1:]:  # Ignorar a primeira coluna ('Nome')
        pivot_df[col] = pd.to_numeric(pivot_df[col], downcast='integer')

    # Adicionando a coluna 'Total de Commits'
    pivot_df['Total de Commits'] = pivot_df.iloc[:, 1:].sum(axis=1)

    return df, pivot_df


def lines_table(users):
    datas = []

    for user in users:
        name = user['name']  # Usando o nome do usuário
        user_months = user.get('month_contributions', {})
        for month, details in user_months.items():
            datas.append({
                'name': name,
                'month': month,
                'lines_modified': details['lines_modified'],  # Focando em 'lines_modified'
                })

    df = pd.DataFrame(datas)
    df['month'] = pd.to_datetime(df['month'])
    df.sort_values(by=['name', 'month'], inplace=True)
    df['month'] = df['month'].dt.strftime('%Y-%m')

    # Pivoteando o DataFrame para focar em "Linhas Modificadas"
    pivot_df = df.pivot_table(index='name', columns='month', values='lines_modified', aggfunc='sum').fillna(0)
    pivot_df.columns.name = None
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'name': 'Nome'}, inplace=True)
    pivot_df.rename(columns=months_pt_br, inplace=True)

    # Convertendo os valores para inteiros e adicionando 'Total de Linhas Modificadas'
    for col in pivot_df.columns[1:]:  # Ignorar a primeira coluna ('Nome')
        pivot_df[col] = pd.to_numeric(pivot_df[col], downcast='integer')

    pivot_df['Total de Linhas Modificadas'] = pivot_df.iloc[:, 1:].sum(axis=1)

    return df, pivot_df


def issue_table(users):
    # Preparando os dados
    datas = [{
        'Nome': user['name'],
        'Issues Atribuídas': user['issues_assigned'],
        'Issues Fechadas': user['issues_closed'],
        'Média de Tempo (s)': user['avg_issue']  # Tempo em segundos, ajuste conforme necessário
        } for user in users]

    # Convertendo para DataFrame
    df = pd.DataFrame(datas)

    # Convertendo a média de tempo de segundos para dias, se necessário
    df['Média de Tempo (dias)'] = df['Média de Tempo (s)'] / 86400
    df.drop(columns=['Média de Tempo (s)'], inplace=True)  # Removendo a coluna de segundos

    # Ordenando por 'Issues Fechadas' para destacar os maiores contribuidores
    df.sort_values(by='Issues Fechadas', ascending=False, inplace=True)

    # Salvar o DataFrame como um arquivo Excel
    # df.to_excel("Issues_Report.xlsx", index=False)

    return df
