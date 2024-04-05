import seaborn as sns
import matplotlib.pyplot as plt


months_pt_br = {
        '2024-01': 'Janeiro', '2024-02': 'Fevereiro', '2024-03': 'Março',
        '2024-04': 'Abril', '2024-05': 'Maio', '2024-06': 'Junho',
        '2024-07': 'Julho', '2024-08': 'Agosto', '2024-09': 'Setembro',
        '2024-10': 'Outubro', '2024-11': 'Novembro', '2024-12': 'Dezembro'
        }


def commit_plots(df, project_name):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 10))
    df['month'] = df['month'].map(months_pt_br)

    # Criação do gráfico com Seaborn
    ax = sns.barplot(data=df, x='name', y='commits', hue='month', dodge=True, palette='coolwarm')
    sns.despine(offset=10, trim=True)  # Remover bordas para um visual mais limpo

    # Ajustes visuais
    ax.set_title(f'Commits por Usuário por Mês', fontsize=16)
    ax.set_xlabel('Usuário', fontsize=14)
    ax.set_ylabel('Número de Commits', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(title='Mês', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    plt.tight_layout()
    plt.savefig("{}_commits_grafico.png".format(project_name))
    plt.close()  # Fecha a figura após salvar para liberar memória


def lines_plots(df, project_name):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 10))
    df['month'] = df['month'].map(months_pt_br)

    # Criação do gráfico com Seaborn focando em "Linhas Modificadas"
    ax = sns.barplot(data=df, x='name', y='lines_modified', hue='month', dodge=True, palette='coolwarm')
    sns.despine(offset=10, trim=True)

    # Ajustes visuais
    ax.set_title(f'Linhas Modificadas por Usuário por Mês', fontsize=16)
    ax.set_xlabel('Usuário', fontsize=14)
    ax.set_ylabel('Linhas Modificadas', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(title='Mês', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    plt.tight_layout()
    plt.savefig("{}_linhas_modificadas_grafico.png".format(project_name))
    plt.close()  # Fecha a figura após salvar para liberar memória


def issues_plots(df, project_name):
    df_melted = df.melt(id_vars=["Nome"], value_vars=["Issues Atribuídas", "Issues Fechadas"],
                        var_name="Tipo de Issue", value_name="Quantidade")

    # Criando o gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_melted, x="Nome", y="Quantidade", hue="Tipo de Issue", palette="coolwarm")

    # Melhorando a apresentação
    plt.title("Comparativo de Issues Atribuídas vs. Issues Fechadas por Usuário")
    plt.xticks(rotation=45)
    plt.ylabel("Quantidade")
    plt.xlabel("Usuário")
    plt.legend(title="Tipo de Issue")

    # Ajustando layout e exibindo o gráfico
    plt.tight_layout()
    plt.savefig("{}_issues_grafico.png".format(project_name))
    plt.close()  # Fecha a figura após salvar para liberar memória


def avg_issue_plots(df, project_name):
    plt.figure(figsize=(10, 6))
    # Utilizando 'color' para definir uma cor uniforme para todas as barras
    sns.barplot(data=df, x="Nome", y="Média de Tempo (dias)", color="c")

    # Melhorando a apresentação
    plt.title("Tempo Médio por Issue entre Usuários")
    plt.xticks(rotation=45)
    plt.ylabel("Média de Tempo (dias)")
    plt.xlabel("Usuário")

    # Ajustando layout e exibindo o gráfico
    plt.tight_layout()
    plt.savefig("{}_issues_avg_grafico.png".format(project_name))
    plt.close()