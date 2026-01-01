from flask import Flask, render_template, request, redirect, session, url_for, flash
from web3 import Web3
from werkzeug.security import generate_password_hash, check_password_hash
import json, os
from functools import wraps
import hashlib
from datetime import timedelta


GANACHE_URL = "http://127.0.0.1:7545"

USERS_FILE = "exported_users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))

            if role and session.get('role') != role:
                return "Unauthorized Access", 403

            return f(*args, **kwargs)
        return wrapped
    return decorator

app = Flask(__name__)
app.secret_key = "blood_donation_blockchain_2025"
app.permanent_session_lifetime = timedelta(minutes=30)


# Blockchain connection
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Ganache
assert w3.is_connected(), "Blockchain not connected"

with open("../build/contracts/UserRegistry.json") as f:
    contract_json = json.load(f)

contract_abi = contract_json["abi"]
contract_address = "0x4211a0a858845d6CD5f2E83F2Ca966D6154b715D"

contract = w3.eth.contract(
    address=contract_address,
    abi=contract_abi
)
backend_account = w3.eth.accounts[0]
account = w3.eth.accounts[0]  # Default sender
# ---------------- HOME ----------------
@app.route("/")
def base():
    return render_template("index.html")

# ---------------- AUTH ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        success, role = contract.functions.loginUser(
            username, password
        ).call()

        if success:
            session.permanent = True
            session['user'] = username
            session['role'] = role.strip().lower()

            return redirect(url_for(session['role']))

        return "Invalid credentials"

    return render_template('login.html')


# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         # Use .transact() instead of .call() to trigger Events
#         try:
#             tx_hash = contract.functions.loginUser(
#                 username, password
#             ).transact({'from': backend_account})
            
#             # Wait for transaction to be mined
#             receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#             # --- LOG PRINTING LOGIC ---
#             # This looks for your "DebugLog" events in the transaction logs
#             if hasattr(contract.events, 'DebugLog'):
#                 logs = contract.events.DebugLog().process_receipt(receipt)
#                 for log in logs:
#                     print(f"BLOCKCHAIN LOG: {log['args']['message']} -> {log['args']['value']}")

#             if hasattr(contract.events, 'DebugHash'):
#                 hash_logs = contract.events.DebugHash().process_receipt(receipt)
#                 for log in hash_logs:
#                     print(f"BLOCKCHAIN HASH: {log['args']['message']} -> {log['args']['value'].hex()}")
#             # -------------------------

#             # We still need to get the result values
#             success, role = contract.functions.loginUser(username, password).call()
            
#             if success:
#                 session.permanent = True
#                 session['user'] = username
#                 session['role'] = role
#                 return redirect(f'/{role}')

#         except Exception as e:
#             print(f"Error during login transaction: {e}")

#         return "Invalid credentials"

#     return render_template('login.html')





# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         name = request.form["name"]
#         role = request.form["role"]

#         tx_hash = contract.functions.registerUser(
#             name, role
#         ).transact({
#     "from": account,
#     "gas": 3000000
# })

#         account = w3.eth.accounts[0]


#         w3.eth.wait_for_transaction_receipt(tx_hash)

#         flash("User Registered on Blockchain!")
#         return redirect("/login")

#     return render_template("register.html")

users_db = {}  # temporary (off-chain)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        name = request.form.get('username')
        print(name,"username")
        raw_password = request.form.get('password')
        password = hashlib.sha256(raw_password.encode()).hexdigest()
        print(raw_password,"pass")
        role = request.form.get('role')
        print(role,"role")

        if not name or not password or not role:
            return "Missing fields"

        try:
            contract.functions.registerUser(
                name, raw_password, role
            ).transact({'from': backend_account})

            return redirect('/login')

        except Exception as e:
            return f"Registration failed: {str(e)}"

    return render_template('register.html')

# @app.route("/register", methods=["POST"])
# def register():
#     try:
#         name = request.form["name"]
#         role = request.form["role"]

#         tx_hash = contract.functions.registerUser(
#             name,
#             role
#         ).transact({
#             "from": w3.eth.accounts[0],
#             "gas": 3000000
#         })

#         w3.eth.wait_for_transaction_receipt(tx_hash)

#         return "✅ User registered successfully on Blockchain"

#     except Exception as e:
#         print("ERROR:", e)
#         return f"❌ Registration failed: {str(e)}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- DASHBOARDS ----------------
@app.route("/donor")
@login_required("donor")
def donor():
    return render_template("donor.html")

@app.route("/hospital")
@login_required("hospital")
def hospital():
    return render_template("hospital.html")

@app.route("/lab")
@login_required("lab")
def lab():
    return render_template("lab.html")

@app.route("/bloodbank")
@login_required("bloodbank")
def bloodbank():
    return render_template("bloodbank.html")

@app.route("/health")
@login_required("health")
def health():
    return render_template("health.html")

@app.route("/patient")
@login_required("patient")
def patient():
    return render_template("patient.html")

@app.route("/logistics")
@login_required("logistics")
def logistics():
    return render_template("logistics.html")

# @app.route("/donor")
# @login_required("donor")
# def donor():
#     return render_template(
#         "dashboard.html",
#         title="Donor Dashboard",
#         latest_block=w3.eth.block_number,
#         tx_count=w3.eth.get_block_transaction_count(w3.eth.block_number),
#         transactions=[]
#     )

# @app.route("/hospital")
# @login_required("hospital")
# def hospital():
#     return render_template(
#         "dashboard.html",
#         title="Hospital Dashboard",
#         latest_block=w3.eth.block_number,
#         tx_count=w3.eth.get_block_transaction_count(w3.eth.block_number),
#         transactions=[]
#     )

# @app.route("/lab")
# @login_required("lab")
# def lab():
#     return render_template(
#         "dashboard.html",
#         title="Lab Dashboard",
#         latest_block=w3.eth.block_number,
#         tx_count=w3.eth.get_block_transaction_count(w3.eth.block_number),
#         transactions=[]
#     )

# @app.route("/bloodbank")
# @login_required("bloodbank")
# def bloodbank():
#     return render_template(
#         "dashboard.html",
#         title="Blood Bank Dashboard",
#         latest_block=w3.eth.block_number,
#         tx_count=w3.eth.get_block_transaction_count(w3.eth.block_number),
#         transactions=[]
#     )
    
# @app.route("/health")
# @login_required("health")
# def health():
#     return render_template(
#         "dashboard.html",
#         title="Health Authority Dashboard",
#         latest_block=w3.eth.block_number,
#         tx_count=w3.eth.get_block_transaction_count(w3.eth.block_number),
#         transactions=[]
#     )
    
# @app.route("/patient")
# @login_required("patient")
# def patient():
#     return render_template(
#         "dashboard.html",
#         title="Patient Dashboard",
#         latest_block=w3.eth.block_number,
#         tx_count=w3.eth.get_block_transaction_count(w3.eth.block_number),
#         transactions=[]
#     )
    
# @app.route("/logistics")
# @login_required("logistics")
# def logistics():
#     return render_template(
#         "dashboard.html",
#         title="Logistics Dashboard",
#         latest_block=w3.eth.block_number,
#         tx_count=w3.eth.get_block_transaction_count(w3.eth.block_number),
#         transactions=[]
#     )
# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
