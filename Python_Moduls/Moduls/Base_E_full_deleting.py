from pymongo import MongoClient


def total_delete_E():
    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    employees.delete_many({})

    print('Проверим есть ли записи после очистки. Они выведутся если есть. ')
    for employee in employees.find({}):
        print(employee)
    print('База очищена.')



if __name__ == '__mane__':
    total_delete()
    # check base
    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    for employee in employees.find({}):
        print(employee)