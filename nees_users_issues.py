import datetime


def update_users_data(user_data, issue, issue_closed, issue_create_date_str):
    user_data['issues_assigned'] += 1

    if issue_closed:
        user_data['issues_closed'] += 1
        # Convertendo strings para objetos datetime
        issue_create_date = datetime.datetime.fromisoformat(issue_create_date_str)
        issue_close_date_str = issue.closed_at or datetime.datetime.now().isoformat()
        issue_close_date = datetime.datetime.fromisoformat(issue_close_date_str)

        # Calculando a duração
        issue_duration = issue_close_date - issue_create_date
        total_issue_time = user_data['avg_issue'] * (user_data['issues_closed'] - 1)
        user_data['avg_issue'] = (total_issue_time + issue_duration.total_seconds()) / user_data['issues_closed']


def issues_by_user(gl, projects_id, users_data, start_day):
    # Inicializar um dicionário para rastrear se um usuário teve issues atribuídas
    users_with_issues = {str(user_data['id']): False for user_data in users_data}

    for project_id in projects_id:
        project = gl.projects.get(project_id)
        issues = project.issues.list(all=True, updated_after=start_day)
        for issue in issues:
            if issue.assignee and issue.assignee['id']:
                user_id_str = str(issue.assignee['id'])
                if user_id_str in users_with_issues:
                    # Marca o usuário como tendo uma issue atribuída
                    users_with_issues[user_id_str] = True
                    for user_data in users_data:
                        if str(user_data['id']) == user_id_str:
                            update_users_data(user_data, issue, issue.state == 'closed', issue.created_at)

    # Filtra users_data para incluir apenas usuários que tiveram issues atribuídas
    filtered_users_data = [user_data for user_data in users_data if users_with_issues[str(user_data['id'])]]

    return filtered_users_data


def users_issues_print(users_data):
    for user in users_data:
        if user['issues_assigned'] > 0 or user['issues_closed'] > 0:
            print(f"Usuário: {user['name']}")
            print(f"Issues Atribuídas: {user['issues_assigned']}, Issues Fechadas: {user['issues_closed']}")
            if user['issues_closed'] > 0:
                # Convertendo segundos para um formato legível (dias, hh:mm:ss)
                avg_time = datetime.timedelta(seconds=user['avg_issue'])
                print(f"Tempo Médio por Issue (dias, hh:mm:ss): {avg_time}")
            print("-" * 30)
