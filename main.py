import datetime as dt
import pprint as pp

# Constants
LOAN_AMOUNT = 20640
LOAN_DATE = dt.datetime(2022,9,13)
INTEREST_RATE = 0.0899
DAYS_PER_YEAR = 365
INTEREST_PER_DAY = INTEREST_RATE/DAYS_PER_YEAR
# Payment Types
REGULAR = "Regular"
EXTRA = "Extra"
INTEREST = "Interest"

total_interest = 0
total_regular_payments = 0
total_extra_payments = 0
payments = [
    {
        "Date": dt.datetime(2022,9,26),
        "Amount": 516,
        "Type": EXTRA
    },
    {
        "Date": dt.datetime(2022,9,30),
        "Type": INTEREST
    },
    {
        "Date": dt.datetime(2022,10,1),
        "Amount": 90.87,
        "Type": REGULAR
    },
    {
        "Date": dt.datetime(2022,10,7),
        "Amount": 516,
        "Type": EXTRA
    },
    {
        "Date": dt.datetime(2022,10,16),
        "Amount": 563.46,
        "Type": EXTRA
    },
    {
        "Date": dt.datetime(2022,10,31),
        "Type": INTEREST
    },
    {
        "Date": dt.datetime(2022,11,1),
        "Amount": 513.53,
        "Type": REGULAR
    },
    {
        "Date": dt.datetime(2022,11,4),
        "Amount": 75,
        "Type": EXTRA
    },
    {
        "Date": dt.datetime(2022,11,6),
        "Amount": 5,
        "Type": EXTRA
    },
    {
        "Date": dt.datetime(2022,11,30),
        "Type": INTEREST
    },
]

def main():
    global total_interest
    for i, payment in enumerate(payments):
        # Calculate the delta between the last two dates
        if i == 0:
            delta = payment["Date"] - LOAN_DATE
            new_payment = apply_payment(payment["Date"], LOAN_AMOUNT, delta.days, payment["Amount"], payment["Type"])
            # print(f"New Payment: {new_payment}")
            payment["Interest"] = new_payment["Interest"]
            payment["Balance"] = new_payment["Balance"]
            print(f"Payment: {payment}")
        else:
            delta = payment["Date"] - payments[i-1]["Date"]
            
            if payment["Type"] == INTEREST:
                new_interest = apply_interest(payment["Date"], payments[i-1]["Balance"], delta.days)
                # print(f"New Payment: {new_interest}")
                payment["Interest"] = new_interest["Interest"]
                payment["Total Interest"] = calculate_total_interest(payment["Date"])
                total_interest += payment["Total Interest"]
                # Calculate the new balance after having the total interest amount
                payment["Balance"] = round(payments[i-1]["Balance"] + payment["Total Interest"], 2)
                # print(f"Balance: {payment["Balance"]}")
                print(f"Payment: {payment}")
            elif payment["Type"] in [REGULAR, EXTRA]:
                days = delta.days
                if payments[i-1]["Type"] == INTEREST:   # Discount the extra day from the last interest
                    days = delta.days - 1
                new_payment = apply_payment(payment["Date"], payments[i-1]["Balance"], days, payment["Amount"], payment["Type"])
                # print(f"New Payment: {new_payment}")
                payment["Interest"] = new_payment["Interest"]
                payment["Balance"] = new_payment["Balance"]
                print(f"Payment: {payment}")

        # switch

        # payment["Interest"] = LOAN_AMOUNT * INTEREST_PER_DAY * delta.days
        # print(payment["Interest"])
        # payment["Balance"] = LOAN_AMOUNT - payment["Extra"]
        # pp.pprint(payment)
    print_totals()

def apply_payment(date, balance, delta_days, amount, type):
    global total_regular_payments, total_extra_payments
    interest = balance * INTEREST_PER_DAY * delta_days
    # print(f"Interest: {interest}")
    new_balance = balance - amount
    # print(f"Balance: {new_balance}")
    new_payment = {
        "Date": date,
        "Extra": amount,
        "Type": type,
        "Interest": round(interest, 2),
        "Balance": round(new_balance, 2)  #"${:,.2f}".format(new_balance)
    }
    if type == REGULAR:
        total_regular_payments += amount
    elif type == EXTRA:
        total_extra_payments += amount
    return new_payment

def apply_interest(date, balance, delta_days):
    interest = balance * INTEREST_PER_DAY * (delta_days + 1)    # Delta_Days increased by 1 when interest calculation
    # print(f"Interest: {interest}")
    new_interest = {
        "Date": date,
        "Type": INTEREST,
        "Interest": round(interest, 2)
    }
    return new_interest

def calculate_total_interest(date):
    month_payments = [payment["Interest"] for payment in payments if date.month == payment["Date"].month]
    total_interest = sum(month_payments)
    # print(total_interest)
    return total_interest

def print_totals():
    global total_regular_payments, total_extra_payments, total_interest
    print(f"Total Interest: " + "${:,.2f}".format(total_interest))
    print(f"Total {REGULAR} payments: " + "${:,.2f}".format(total_regular_payments))
    print(f"Total {EXTRA} payments: " + "${:,.2f}".format(total_extra_payments))
    print(f"Total Payments: " + "${:,.2f}".format(total_regular_payments + total_extra_payments))

if __name__ == "__main__":
    main()
