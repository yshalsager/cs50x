import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    current_stocks = db.execute("SELECT stock FROM transactions WHERE id = :id GROUP BY stock",
                                id=user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
    grand_total = cash[0]["cash"]
    if not current_stocks:
        return render_template("index.html", cash=usd(cash[0]["cash"]), grand_total=usd(grand_total))

    items = []
    for stock in current_stocks:
        data = lookup(stock["stock"])
        current_price = data["price"]
        stock_info = {}
        shares_info = db.execute("SELECT SUM(shares) AS shares_sum FROM transactions WHERE id = :id\
                                GROUP BY stock HAVING stock = :symbol", id=user_id, symbol=stock["stock"])
        current_shares = shares_info[0]["shares_sum"]
        if current_shares > 0:
            stock_info["symbol"] = stock["stock"]
            stock_info["name"] = data["name"]
            stock_info["price"] = usd(current_price)
            stock_info["shares"] = current_shares
            total = current_price * current_shares
            grand_total += total
            stock_info["total"] = usd(total)
            items.append(stock_info)
    return render_template("index.html", storages=items, cash=usd(cash[0]["cash"]), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Missing symbol!", 400)
        data = lookup(symbol)
        if not data:
            return apology("Invalid symbol!", 400)
        if not request.form.get("shares").isdigit():
            return apology("Shares must be a positive number", 400)
        shares = float(request.form.get("shares"))
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        money = cash[0]["cash"]
        price = data["price"]
        amount = price * shares
        if money < amount:
            return apology("Can't afford buying!", 400)
        else:
            db.execute("INSERT INTO transactions (id, stock, shares, price, total)\
                       VALUES(:id, :stock, :shares, :price, :total)",
                       id=user_id, stock=data["symbol"],
                       shares=shares, price=price, total=amount)
            balance = money - amount
            db.execute("UPDATE users SET cash = :balance WHERE id = :id",
                       balance=balance, id=user_id)
            flash("Bought Successfully!")
            return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    user = request.args.get("username")
    if db.execute("SELECT * FROM users WHERE username = :username",
                  username=user):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history_ = db.execute("SELECT * FROM transactions WHERE id=:id", id=session["user_id"])
    return render_template("history.html", history=history_)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        data = lookup(request.form.get("symbol"))
        if not data:
            return apology("Invalid symbol", 400)
        else:
            data["price"] = usd(float(data["price"]))
            return render_template("quoted.html", stock=data)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("You must provide an username!", 400)
        elif not password:
            return apology("You must provide a password!", 400)
        elif not request.form.get("confirmation"):
            return apology("You must confirm the password!", 400)
        elif password != request.form.get("confirmation"):
            return apology("Password and confirmation does not match", 400)
        elif db.execute("SELECT * FROM users WHERE username = :username",
                        username=username):
            return apology("Username already exists", 400)
        password_hash = generate_password_hash(password)
        table = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=password_hash)
        session["user_id"] = table
        flash("Registered!")
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    current_stocks = db.execute("SELECT stock FROM transactions WHERE id = :id GROUP BY stock",
                                id=user_id)
    if request.method == "GET":
        list_symbols = list()
        for symbol in current_stocks:
            shares_info = db.execute("SELECT SUM(shares) AS shares_sum FROM transactions\
                                    WHERE id = :id GROUP BY stock HAVING stock = :stock",
                                     id=user_id, stock=symbol["stock"])
            if shares_info[0]["shares_sum"]:
                list_symbols.append(symbol["stock"])
        return render_template("sell.html", list_symbols=list_symbols)
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("SYMBOL CAN'T BE EMPTY", 400)
        if not request.form.get("shares"):
            return apology("SHARES CAN'T BE EMPTY", 400)
        shares = float(request.form.get("shares"))
        shares_info = db.execute("SELECT SUM(shares) AS shares_sum FROM transactions\
                                    WHERE id = :id GROUP BY stock HAVING stock = :stock", id=user_id, stock=symbol)
        if shares_info[0]["shares_sum"] < shares:
            return apology("SHARES CAN'T BE MORE THAN WHAT YOU HAVE", 400)
        else:
            data = lookup(symbol)
            price = data["price"]
            money = -shares * price
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
            balance = cash[0]["cash"] - money
            db.execute("INSERT INTO transactions (id, stock, shares, price, total)\
                        VALUES(:id, :stock, :shares, :price, :total)",
                       id=user_id, stock=symbol, shares=-shares, price=price, total=money)
            db.execute("UPDATE users SET cash = :balance WHERE id = :id", balance=balance, id=user_id)
            flash("Sold")
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
