const user_input = document.getElementById("user");
const password_input = document.getElementById("password");
const login_fields = document.getElementById("login-fields");
const login_section = document.getElementById("login-section");

login_section.style.display = "none";

const user_type_options = document.querySelectorAll('input[name="user-type"]');

const placeholders_dict = {
    optGovernamental: {
        user: "Digite sua matrícula...",
        password: "Digite sua senha..."
    },
    optEmpresarial: {
        user: "Digite o CNPJ da empresa...",
        password: "Digite a senha de acesso da empresa..."
    }
};

function updateInputRequiredAttributeStatus(user_type_id) {
    const isCivil = user_type_id === "optCivil";
    user_input.required = !isCivil;
    password_input.required = !isCivil;
    user_input.disabled = isCivil;
    password_input.disabled = isCivil;
}

function updateAplicationEntranceMethod(user_type_id) {
    login_section.style.display = "block";
    if (user_type_id == "optCivil") {
        login_fields.style.display = "none";
    } else {
        login_fields.style.display = "block";
        user_input.placeholder = placeholders_dict[user_type_id]["user"];
        password_input.placeholder = placeholders_dict[user_type_id]["password"];
    }
};

function displayAplicationEntranceMethod() {
    let selected_user_type = document.querySelectorAll('input[name="user-type"]');
    selected_user_type.forEach((option) => {
        option.addEventListener("click", () => {
            updateInputRequiredAttributeStatus(option.id)
            updateAplicationEntranceMethod(option.id);
        })
    });
}

displayAplicationEntranceMethod();