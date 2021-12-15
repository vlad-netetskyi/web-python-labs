import json
from app.forms import LoginFormSecond


def writeToFile(form: LoginFormSecond):
    login = form.login.data
    data = {
        login: {
            "password": form.password.data,
            "Examenation list number": form.e_l_number.data,
            "Examenation list PIN": form.e_l_pin.data,
            "Examenation list year": form.e_l_year.data,
            "Document education series": form.d_f_e_series.data,
            "Document education number": form.d_f_e_number.data
        },
    }
    try:
        with open('users.json') as f:
            data_files = json.load(f)
            data_files.update(data)

            with open('users.json', 'w', encoding='utf-8') as f:
                json.dump(data_files, f, ensure_ascii=False, indent=4)
    except:
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
