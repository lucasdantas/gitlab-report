import os
import json
import gitlab
from openpyxl.workbook import Workbook
from nees_tables import commit_table, lines_table, issue_table
from nees_users_contributions import users_contributions
from nees_users_create import create_users
from nees_file_generator import file_generator
from nees_users_issues import issues_by_user

from settings import (
    GL_URL,
    PROJECTS_ID,
    PRIVATE_TOKEN,
    START_DAY,
    MULTIPLE_ACCOUNT_MAPPING,
)


def main():
    gl = gitlab.Gitlab(GL_URL, private_token=PRIVATE_TOKEN)
    USERS_DATA_FILE = "users_data.json"

    for project_id in PROJECTS_ID:

        project = gl.projects.get(project_id)

        # Verifica se o arquivo USERS_DATA_FILE existe
        if os.path.isfile(USERS_DATA_FILE):
            with open(USERS_DATA_FILE, "r") as f:
                users_data = json.load(f)
        else:
            users_data = create_users(
                gl,
                PROJECTS_ID,
                START_DAY,
                MULTIPLE_ACCOUNT_MAPPING if MULTIPLE_ACCOUNT_MAPPING else None,
            )

            with open(USERS_DATA_FILE, "w") as f:
                json.dump(users_data, f, indent=4)

        wb = Workbook()

        if "Sheet" in wb.sheetnames:
            del wb["Sheet"]

        # Código para gerar relatórios, agora passando o wb e nomes de sheets como argumentos
        users = users_contributions(gl, PROJECTS_ID, users_data, START_DAY)
        users = issues_by_user(gl, PROJECTS_ID, users, START_DAY)

        # Commits
        df, pivot_df = commit_table(users)
        file_generator(wb, "Commits", pivot_df, df, "commits", project.name)

        # Linhas Modificadas
        df, pivot_df = lines_table(users)
        file_generator(
            wb, "Linhas Modificadas", pivot_df, df, "lines_modified", project.name
        )

        # Média de Issues
        df = issue_table(users)
        file_generator(wb, "Tempo Médio por Issue", df, df, "avg_issue", project.name)

        # Issues Atribuídas
        df = issue_table(users)
        file_generator(
            wb, "Issues por Usuário", df, df, "issues_assigned", project.name
        )

        # Salvando o arquivo após todas as sheets terem sido adicionadas
        wb.save(f"Relatório {project.name}.xlsx")

        print(f"Relatório {project.name} gerado com sucesso!")


if __name__ == "__main__":
    main()
