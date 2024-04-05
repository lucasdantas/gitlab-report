from datetime import datetime


def find_user_by_email(users_data, email):
    for index, user in enumerate(users_data):
        if email in user['email']:
            return index  # Retorna o índice do usuário no dicionário
    return None


def month_contributions_update(users_data, user_index, commit_date, additions, deletions):
    year_month = commit_date.strftime('%Y-%m')
    contributions = users_data[user_index].get('month_contributions', {}).get(year_month,
                                                                  {'commits': 0, 'lines_modified': 0, 'lines_added': 0,
                                                               'lines_deleted': 0})

    contributions['commits'] += 1
    contributions['lines_modified'] += additions + deletions
    contributions['lines_added'] += additions
    contributions['lines_deleted'] += deletions

    if 'month_contributions' not in users_data[user_index]:
        users_data[user_index]['month_contributions'] = {}
    users_data[user_index]['month_contributions'][year_month] = contributions


def users_contributions(gl, projects_id, users_data, start_day):
    for project_id in projects_id:
        project = gl.projects.get(project_id)
        branches = project.branches.list(all=True)
        since_date = datetime.strptime(start_day, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        for branch in branches:
            commits_ids = project.commits.list(all=True,
                                               query_parameters={'since': since_date, 'ref_name': branch.name})
            for commit_id in commits_ids:
                commit = project.commits.get(commit_id.id)
                author_email = commit.author_email
                commit_date = datetime.strptime(commit.created_at, '%Y-%m-%dT%H:%M:%S.%f%z')
                user_index = find_user_by_email(users_data, author_email)
                if user_index is not None:
                    stats = commit.stats
                    users_data[user_index]['lines_added'] += stats['additions']
                    users_data[user_index]['lines_deleted'] += stats['deletions']
                    users_data[user_index]['lines_modified'] += stats['additions'] + stats['deletions']
                    month_contributions_update(users_data, user_index, commit_date, stats['additions'], stats['deletions'])

    # Filtrando para retornar apenas usuários que possuem linhas modificadas ou commits
    filtered_users_data = [user for user in users_data if user.get('lines_modified', 0) > 0]

    return filtered_users_data


def users_contributions_print(users_data):
    for user in sorted(users_data, key=lambda x: x['name']):
        if 'month_contributions' in user and any(
                contrib['commits'] > 0 for contrib in user['month_contributions'].values()):
            print(f"{user['name']}:")
            for year_month, contribuicoes in sorted(user['month_contributions'].items()):
                print(
                    f"  {year_month}: Commits: {contribuicoes['commits']}, Linhas Modificadas: "
                    f"{contribuicoes['lines_modified']}, Linhas Adicionadas: {contribuicoes['lines_added']}, "
                    f"Linhas Deletadas: {contribuicoes['lines_deleted']}")
