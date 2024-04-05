from datetime import datetime


def create_users(gl, project_ids, start_date, email_to_user_mapping=None):
    users_data = []

    for project_id in project_ids:
        project = gl.projects.get(project_id)
        members = project.members.list(all=True)
        name_to_index = {}
        username_to_index = {}

        for member in members:
            user = gl.users.get(member.id)
            name_to_index[user.name] = len(users_data)
            username_to_index[user.username] = len(users_data)

            users_data.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "name": user.name,
                    "email": [],
                    "commits": 0,
                    "lines_modified": 0,  # Isso agora será calculado
                    "lines_added": 0,
                    "lines_deleted": 0,
                    "issues_assigned": 0,
                    "issues_closed": 0,
                    "avg_issue": 0,
                }
            )

        # Processando commits
        commits = project.commits.list(since=start_date, all=True)
        for commit in commits:
            commit_detail = project.commits.get(
                commit.id, statistics=True
            )  # Pedindo estatísticas
            author_name = commit_detail.author_name
            author_email = commit_detail.author_email

            # Determinando o índice do usuário correto
            user_index = None
            if email_to_user_mapping and author_email in email_to_user_mapping:
                username = email_to_user_mapping[author_email]
                if username in username_to_index:
                    user_index = username_to_index[username]
            if user_index is None and author_name in name_to_index:
                user_index = name_to_index[author_name]

            # Atualizando dados do usuário
            if user_index is not None:
                users_data[user_index]["commits"] += 1
                if author_email not in users_data[user_index]["email"]:
                    users_data[user_index]["email"].append(author_email)
                # Atualizando linhas adicionadas e deletadas
                users_data[user_index]["lines_added"] += commit_detail.stats[
                    "additions"
                ]
                users_data[user_index]["lines_deleted"] += commit_detail.stats[
                    "deletions"
                ]
                # Linhas modificadas são a soma de adicionadas e deletadas
                users_data[user_index]["lines_modified"] = (
                    users_data[user_index]["lines_added"]
                    + users_data[user_index]["lines_deleted"]
                )

    users_with_contributions = [
        user
        for user in users_data
        if user["commits"] > 0 or user["lines_added"] > 0 or user["lines_deleted"] > 0
    ]
    return users_with_contributions


def members_list(gl, projects_id):
    projects_members = {}

    for project_id in projects_id:
        project = gl.projects.get(project_id)
        members = project.members.list(all=True)
        projects_members[project.name] = [
            print({"id": member.id, "name": member.name, "username": member.username})
            for member in members
        ]

    return projects_members


def commits_authors(gl, projects_id, start_day, only_email=True):
    authors_list = []
    unique_authors = set()  # Um conjunto para armazenar os autores únicos
    current_day = datetime.now().strftime(
        "%Y-%m-%d"
    )  # Data atual no formato YYYY-MM-DD

    for project_id in projects_id:
        project = gl.projects.get(project_id)
        commits = project.commits.list(since=start_day, until=current_day, all=True)

        for commit in commits:
            autor = commit.author_name
            # Verifica se o autor já foi adicionado
            if autor not in unique_authors:
                unique_authors.add(autor)

                if only_email:
                    authors_list.append({"author_email": commit.author_email})
                else:
                    authors_list.append(
                        {
                            "author_name": commit.author_name,
                            "author_email": commit.author_email,
                        }
                    )

    return authors_list
