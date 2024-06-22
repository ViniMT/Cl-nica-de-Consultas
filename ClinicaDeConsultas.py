import pickle
import os
from datetime import datetime

# Arquivos para armazenar os dados
PACIENTES_FILE = 'pacientes.pkl'
AGENDAMENTOS_FILE = 'agendamentos.pkl'

# Carregar dados de pacientes e agendamentos
def carregar_dados():
    if os.path.exists(PACIENTES_FILE):
        with open(PACIENTES_FILE, 'rb') as f:
            pacientes = pickle.load(f)
    else:
        pacientes = []

    if os.path.exists(AGENDAMENTOS_FILE):
        with open(AGENDAMENTOS_FILE, 'rb') as f:
            agendamentos = pickle.load(f)
    else:
        agendamentos = []

    return pacientes, agendamentos

# Salvar dados de pacientes e agendamentos
def salvar_dados(pacientes, agendamentos):
    with open(PACIENTES_FILE, 'wb') as f:
        pickle.dump(pacientes, f)

    with open(AGENDAMENTOS_FILE, 'wb') as f:
        pickle.dump(agendamentos, f)

# Função para cadastrar paciente
def cadastrar_paciente(pacientes, agendamentos):
    nome = input("Digite o nome do paciente: ")
    telefone = input("Digite o telefone do paciente: ")

    for paciente in pacientes:
        if paciente['telefone'] == telefone:
            print("Paciente já cadastrado!")
            return

    pacientes.append({'nome': nome, 'telefone': telefone})
    print("Paciente cadastrado com sucesso!")
    salvar_dados(pacientes, agendamentos)

# Função para marcar consulta
def marcar_consulta(pacientes, agendamentos):
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return

    print("Pacientes cadastrados:")
    for i, paciente in enumerate(pacientes):
        print(f"{i + 1}. {paciente['nome']} - {paciente['telefone']}")

    paciente_idx = int(input("Escolha o número do paciente: ")) - 1

    if paciente_idx < 0 or paciente_idx >= len(pacientes):
        print("Paciente inválido.")
        return

    paciente = pacientes[paciente_idx]
    dia = input("Digite o dia da consulta (dd/mm/aaaa): ")
    hora = input("Digite a hora da consulta (HH:MM): ")
    especialidade = input("Digite a especialidade da consulta: ")

    # Verificar se a data e hora são válidas
    data_consulta = datetime.strptime(f"{dia} {hora}", "%d/%m/%Y %H:%M")
    if data_consulta <= datetime.now():
        print("Não é possível marcar consultas retroativas.")
        return

    for agendamento in agendamentos:
        if agendamento['dia'] == dia and agendamento['hora'] == hora:
            print("Já existe uma consulta marcada para este horário.")
            return

    agendamentos.append({'paciente': paciente, 'dia': dia, 'hora': hora, 'especialidade': especialidade})
    print("Consulta marcada com sucesso!")
    salvar_dados(pacientes, agendamentos)

# Função para cancelar consulta
def cancelar_consulta(agendamentos):
    if not agendamentos:
        print("Nenhum agendamento existente.")
        return

    print("Agendamentos existentes:")
    for i, agendamento in enumerate(agendamentos):
        paciente = agendamento['paciente']
        print(f"{i + 1}. {paciente['nome']} - {agendamento['dia']} {agendamento['hora']} - {agendamento['especialidade']}")

    agendamento_idx = int(input("Escolha o número do agendamento para cancelar: ")) - 1

    if agendamento_idx < 0 or agendamento_idx >= len(agendamentos):
        print("Agendamento inválido.")
        return

    agendamento = agendamentos.pop(agendamento_idx)
    print(f"Consulta de {agendamento['paciente']['nome']} no dia {agendamento['dia']} às {agendamento['hora']} foi cancelada.")
    salvar_dados(pacientes, agendamentos)

# Menu principal
def menu():
    pacientes, agendamentos = carregar_dados()

    while True:
        print("\nClínica de Consultas Ágil")
        print("1. Cadastrar paciente")
        print("2. Marcar consulta")
        print("3. Cancelar consulta")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_paciente(pacientes, agendamentos)
        elif opcao == '2':
            marcar_consulta(pacientes, agendamentos)
        elif opcao == '3':
            cancelar_consulta(agendamentos)
        elif opcao == '4':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
